## Takehome

### This Project Has Got Problems

There are a number of issues with this project.  The goal is to identify and fix as many of the problems as you can and get it to deploy to kubernetes successfully.  If you don't feel like fixing a particular problem, just write down what you would have done so we can discuss it together.

If you don't have a kubernetes cluster handy, you can deploy one locally with [kind](https://kind.sigs.k8s.io/).

Please don't take this as a reflection of the work we do here.  We promise it's not this bad. The goal here is to have you show us that you can debug stuff you didn't write and get it working when needed.

If you have worked or are working on something else that you're more interested in or proud of, and that you can share, feel free to send that back instead of completing this project.

1. as im new to k8s i chose to start a EKS cluster using ekscli utility, this seems to give me a basic cluster that can deploy k8's pods fairly successfully.
2. I installed helm and listed the chart, it seems to lint correclty. but it's actual functionality is yet to be discovered.
3. lets run the flask app locally. I'm not familiar with USA state name abbreviations but im pretty sure that MD stands for Maryland. the App returns New York, https://www.faa.gov/air_traffic/publications/atpubs/cnt_html/appendix_a.html confirms my suspicions that this is incorrect.
4. lets look at the db as im pretty sure the incorrect data is there and not in the app code. using DB Browser for sqlite, we cna see that some state 2-letters are correct like AL for Alabama and some are wrong.
4.1 Pensylvania's Ruffled goose is missing the latin name and year. Note to self check if years and names are actually correct.
4.2 knowing that Northern Cardinal is a popular bird in usa and is state bird of several state, matching the table to wikipedia - that seems correct (Illinois, Indiana, Kentucky, N. Carolina, Ohio, Virginia, and West Virginia)
5. in the app the weather bit was not working correctly, i checked the endpoint via just curl and it's working so something is wrong with the code. - the string stubstitution was wrong 1. not using the param 'state' that is initialised in the function and extra {} were messing with it.
6. lets build the docker image for thr flask app - needs a dockerfile
7. build docker image make sure its using port 80
8. upload to my ECR repo
9. lets try to run a helm deployment to my EKS cluster using the image we built
10. modified the values file with ARN of the DOCKER image
11. Run Helm install
12. Check AWS that it deployed OK
13. do the port forwarding helm suggests to do a quick check 
13.1 Get the application URL by running these commands:
  export POD_NAME=$(kubectl get pods --namespace default -l "app.kubernetes.io/name=birds,app.kubernetes.io/instance=birds-1716812234" -o jsonpath="{.items[0].metadata.name}")
  export CONTAINER_PORT=$(kubectl get pod --namespace default $POD_NAME -o jsonpath="{.spec.containers[0].ports[0].containerPort}")
  echo "Visit http://127.0.0.1:8080 to use your application"
  kubectl --namespace default port-forward $POD_NAME 8080:$CONTAINER_PORT

14. test the app curl http://127.0.0.1:8080/AZ

15. Code smells: the get_bird function has no error handling lets add some. lets also add some input validation. we can also make sure that similar inputs like 'md' or 'Md' are equal to the desired "MD" but lets not do this here.
15.1 more code smells: in the get Bird function i chnaged how the query is templated slightly, it should help with sql injection somewhat.









aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin 520686339686.dkr.ecr.eu-west-1.amazonaws.com

docker tag birds:latest 520686339686.dkr.ecr.eu-west-1.amazonaws.com/birds:latest

docker push 520686339686.dkr.ecr.eu-west-1.amazonaws.com/birds:latest

