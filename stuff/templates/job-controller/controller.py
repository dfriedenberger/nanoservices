import uuid

#{imports}

#{init}


#Erzeugung von Jobs, wenn Objekte in der DB geaendert sind

def recv_message(topic : str, msg : str) -> None:
    print("topic",topic,"msg",msg)
    if topic == "/db/media/create":
        # create job
        
        job = {
            "id" : str(uuid.uuid4()),
            "job" : {
                "image" : "frittenburger/vocabulary-download-job:0.0.1", 
                "command" : f"python download_subtitle.py --media-id {msg['id']}",
                "trigger" : topic
            },
            "state" : "INIT"
        }

        jobRepository.create_job(job)


subscriber.listen_to_topic(["/db/media/create","/db/subtitle/create","/test"], recv_message )

#{implementation}

