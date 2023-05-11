# Deployment guide

Build and Push Container to DockerHub

    docker build -f ../backend/Dockerfile -t divyamagwl/invoicy-backend:latest ../backend/

    docker push divyamagwl/invoicy-backend

Delete Secrets (if exists)

    kubectl delete secrets invoicy-backend-prod-env

Create Secrets

    kubectl create secret generic invoicy-backend-prod-env --from-env-file=../backend/invoicy/.env.prod

Delete All Deployments and Services (if exists)

    kubectl delete -f .

Build All Deployments and Services

    kubectl apply -f .

Deployment Status

    kubectl rollout status deployment/invoicy-backend-deployment

Apply Migrations (if needed)

    export POD_LATEST=$(kubectl get pod -l app=invoicy-backend-deployment -o jsonpath="{.items[0].metadata.name}")

    kubectl exec -it $POD_LATEST -- bash /app/migrate.sh


Tunneling Service

    minikube service invoicy-backend-service