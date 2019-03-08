# Rolling out a new version
To test our loadbalancer, we would like to see which pod / container handles our request.
The easiest way to do so is that we return the hostname.

Go ahead and change the app.py like this:

```python
from flask import Flask
import socket
application = Flask(__name__)

@application.route('/')
def hello_world():
    return 'Hello, World!'

@application.route('/test')
def test():
    return 'Everything works as expected.'

@application.route('/info')
def info():
    return socket.gethostname()
```

As you can see /info will return the hostname for us.

After the modification you can get into the python environment and test locally with flask:

```bash
[14:00:26][0][marczis@sonya:/home/marczis/pro/app_dev_k8s/working_dir/python]|master *|{No activity}
pipenv shell
Launching subshell in virtual environment…
 . /home/marczis/.local/share/virtualenvs/python-gJL2SuBN/bin/activate
[14:00:28][0][marczis@sonya:/home/marczis/pro/app_dev_k8s/working_dir/python]|master *|{No activity}
 . /home/marczis/.local/share/virtualenvs/python-gJL2SuBN/bin/activate
[14:00:28][0][marczis@sonya:/home/marczis/pro/app_dev_k8s/working_dir/python]|master *|{No activity}
(python) flask run
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
127.0.0.1 - - [08/Mar/2019 14:00:40] "GET /info HTTP/1.1" 200 -
```

And from an other terminal:

```bash
curl 127.0.0.1:5000/info
sonya
```

Great!

Now build a new version! Just as before run the build script from the docker directory:

```bash
[14:02:03][0][marczis@sonya:/home/marczis/pro/app_dev_k8s/working_dir/docker]|master *|{No activity}
(python) ./build.sh 
Installing dependencies from Pipfile.lock (aa9572)…
  🐍   ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ 7/7 — 00:00:00
Installing dependencies from Pipfile.lock (aa9572)…
  🐍   ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ 7/7 — 00:00:00
All dependencies are now up-to-date!
Sending build context to Docker daemon  6.656kB
Step 1/7 : FROM python:latest
 ---> 32260605cf7a
Step 2/7 : WORKDIR /
 ---> Using cache
 ---> ea78a19e7365
Step 3/7 : ENV GUNICORN_CMD_ARGS="--bind=0.0.0.0 --workers=3"
 ---> Using cache
 ---> 74bf3c84673f
Step 4/7 : CMD gunicorn app
 ---> Using cache
 ---> aa16d51246bc
Step 5/7 : EXPOSE 8000
 ---> Using cache
 ---> 9d108c1e2119
Step 6/7 : ADD app /app
 ---> Using cache
 ---> fed58c780197
Step 7/7 : RUN pip install -r /app/requirements.txt
 ---> Using cache
 ---> 61371c2fb44f
Successfully built 61371c2fb44f
Successfully tagged myapp:latest
```

Create a new tag:
```bash
docker tag myapp:latest marczis/app_dev_k8s:v2
```

And push it:
```bash
[14:02:49][130][marczis@sonya:/home/marczis/pro/app_dev_k8s/working_dir/docker]|master *|{No activity}
(python) docker push marczis/app_dev_k8s:v2
The push refers to repository [docker.io/marczis/app_dev_k8s]
25a3ef4acff2: Layer already exists 
c1f8cfa119e7: Layer already exists 
bb839e9783c7: Layer already exists 
237ce60325c6: Layer already exists 
1b976700da1f: Layer already exists 
bde41e1d0643: Layer already exists 
7de462056991: Layer already exists 
3443d6cf0f1f: Layer already exists 
f3a38968d075: Layer already exists 
a327787b3c73: Layer already exists 
5bb0785f2eee: Layer already exists 
v2: digest: sha256:82e6625347581ef0c410a3a19bb082cea546f28befeb4be41930ee3322ea63d6 size: 2636
```

And now the real thing, tell to k8s that we have a new image for the deployment:

```bash
kubectl set image deployments/myapp myapp=marczis/app_dev_k8s:v2
deployment.extensions/myapp image updated
```

You can monitor the status of the "rollout" by calling this command:

```bash
kubectl rollout status deployment myapp
deployment "myapp" successfully rolled out
```

Okay, so we have the new version rolled out, behind the scene k8s did a real rolling update, if you would have monitor the process by doing constant requests you would have seen that our service was never interrupted, time to test our changes!

```bash
curl 34.76.152.171:8000/info
myapp-5659844ccf-5qvhc
curl 34.76.152.171:8000/info
myapp-5659844ccf-bhq8l
curl 34.76.152.171:8000/info
myapp-5659844ccf-fbbtw
curl 34.76.152.171:8000/info
myapp-5659844ccf-5qvhc
```

As you can see our request ends up on different "hosts" meaning that the loadbalancer is working!
Now there are a couple of more to try out here for "fun".
Lets say something goes sideways with your new image, try to setup a non existing image!

```bash
kubectl set image deployments/myapp myapp=marczis/app_dev_k8s:nonexistingversionforsure
deployment.extensions/myapp image updated
```

Check the rollout status
```
kubectl rollout status deployment myapp
Waiting for deployment "myapp" rollout to finish: 2 out of 4 new replicas have been updated...
```

This command will block until timeout or the rollout done, we already know that something is wrong, but how you can check that?

```bash
kubectl get pods
NAME                     READY     STATUS             RESTARTS   AGE
myapp-5659844ccf-bhq8l   1/1       Running            0          21m
myapp-5659844ccf-fbbtw   1/1       Running            0          21m
myapp-5659844ccf-h7vr9   1/1       Running            0          21m
myapp-57b96c9b65-qqqjb   0/1       ErrImagePull       0          1m
myapp-57b96c9b65-xq8nx   0/1       ImagePullBackOff   0          1m
```

This already tells us what's wrong but lets check the logs
```bash
kubectl logs myapp-57b96c9b65-qqqjb
Error from server (BadRequest): container "myapp" in pod "myapp-57b96c9b65-qqqjb" is waiting to start: trying and failing to pull image
```

Now we have multiple options too, either set the image again, to a right version or just cancel the rollout:
```bash
kubectl rollout undo deployment myapp
deployment.extensions/myapp
```

If you left the ```rollout status``` open, you will see an immediate update:
```bash
Waiting for deployment "myapp" rollout to finish: 2 out of 4 new replicas have been updated...
Waiting for deployment spec update to be observed...
Waiting for deployment "myapp" rollout to finish: 3 out of 4 new replicas have been updated...
Waiting for deployment "myapp" rollout to finish: 3 out of 4 new replicas have been updated...
Waiting for deployment "myapp" rollout to finish: 3 out of 4 new replicas have been updated...
Waiting for deployment "myapp" rollout to finish: 3 of 4 updated replicas are available...
Waiting for deployment "myapp" rollout to finish: 3 of 4 updated replicas are available...
Waiting for deployment "myapp" rollout to finish: 3 of 4 updated replicas are available...
deployment "myapp" successfully rolled out
```

Amazing right? The super nice thing about this, that meanwhile our service was uninterrupted!

So that's all for this exercise I hope it gave you a solid background to start on Kubernetes and to start your developer lifecycle.
A couple of things I plan for this exercise:
 - Setup CI/CD pipeline
 - Auto scaling
 - More complex example with some DB backend
 - More complex example with cookies, sessions, user auth
 - Add how to setup Kubernetes on AWS, GCP, minikube
 - Private registry
 - Windows / MAC examples

 If you feel like, and have some freetime to spare, I would be happy to get other involved, just fork, add your things and make a pull request!