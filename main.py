import os
import ast
import shutil
import logging
from minio import Minio
from minio.error import S3Error
from tts.google_tts import GoogleTts
from quixstreams import Application


def move_file(path_to_audio:str, new_folder_path:str ="temp_tts_audios/") -> str:
    new_path = new_folder_path + path_to_audio

    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
    shutil.move(path_to_audio, new_path)
    
    
    return new_path

def main():
    google_tts = GoogleTts()
    app_consumer = Application(
        broker_address ="localhost:9092",
        loglevel="DEBUG",
        consumer_group = "scripts_video_reader",
        auto_offset_reset = "latest"
    )

    minio_client = Minio(
    "172.19.0.2:9000",
    access_key="AKIAIOSFODNN7EXAMPLE",
    secret_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
    secure=False
)

    with app_consumer.get_consumer() as consumer:
        consumer.subscribe(["scripts_video"])
        while True:
            msg = consumer.poll(1)
            if msg is None:
                print("Waiting...")
            elif msg.error() is not None:
                raise ValueError(msg.error())
            else:
                print("Message value: ", msg.value())
                #key = msg.key().decode("utf8")
                msg_value = msg.value()
                #offset = msg.offset()
                consumer.store_offsets(msg)
                msg_value_json_response = ast.literal_eval(msg_value.decode("utf-8"))
                script = msg_value_json_response["script"]
                tema = msg_value_json_response["tema"]["tema"]
                audio_name = google_tts.generate_tts(script,tema)
                new_audio_path = move_file(audio_name)
                bucket_name = "audios-tts"
                destination_file = audio_name
                """
                found = minio_client.bucket_exists(bucket_name)
                if not found:
                    print("a")
                    minio_client.make_bucket(bucket_name)
                    print("Created Bucket", bucket_name)
                else:
                    print("b")
                    print(f"Bucket: {bucket_name} already exists")
                """
                minio_client.fput_object(
                    bucket_name, destination_file, new_audio_path
                )
                print(
                    f"{new_audio_path}, succesfully uploaded as object: {destination_file}, to bucket: {bucket_name}"
                )
                os.remove(new_audio_path)

                app_producer = Application(
                    broker_address="localhost:9092", loglevel="DEBUG"
                )
                with app_producer.get_producer() as producer:                    
                    producer.produce(
                        topic="audio_subtitles",
                        key = "Ai Subtitles",
                        value = str({"status": "OK", "audio_name": destination_file, "bucket_name": bucket_name})
                    )
                logging.info("Produced. Sleeping..")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    except S3Error as ex:
        print(f"Ocurrió un error con S3 bucekt: {ex}")


