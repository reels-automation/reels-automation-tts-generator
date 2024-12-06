from quixstreams import Application


def main():

    app_producer = Application(broker_address="localhost:9092", loglevel="DEBUG")


    with app_producer.get_producer() as producer:
        while True:
            input("Enviar mensaje de prueba: \n")
            json_data = {"script": "test", "tema": {"tema": "test", "personaje":"test", "author": None}}
            producer.produce(
                topic="scripts_video", key="temas_input_humano", value=str(json_data)
            )


if __name__ == "__main__":
    main()
