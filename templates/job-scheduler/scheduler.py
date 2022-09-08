from time import sleep
import uuid

#{imports}

def call_serverless(docker_image,command):
    client = docker.DockerClient()

    container_name = "job_{}".format(uuid.uuid4())

    #start image
    container = client.containers.run(image = docker_image, name = container_name , command = command, detach =True, remove = True)
    print("status",container.status)

    data = []
    output = container.attach(stdout=True, stream=True, logs=True);
    for line in output:
       data.append(line)
    #stop container
    container.stop()
    print("status",container.status)

    return data



def run_job(job):
    print("run job",job)
    result = call_serverless(job["image"],job["command"])
    print(job["command"]," => ",result)



#get jobs from database
#{init}


#{implementation}

while True:
    jobs = jobRepository.get_init_jobs();
    if len(jobs) == 0:
        print("no jobs")
        sleep(10)
        continue
    job = jobs[0]
    print(job)
    jobRepository.set_job_state(job['id'],'START')
    run_job(job['job'])
    jobRepository.set_job_state(job['id'],'DONE')
    


