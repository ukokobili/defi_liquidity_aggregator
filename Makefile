docker-spin-up:
	docker compose --env-file env up --build -d

sleeper:
	sleep 15

up: docker-spin-up sleeper warehouse-migration

down: 
	docker compose --env-file env down

shell:
	docker exec -ti defi_pipeline bash

format:
	docker exec defi_pipeline python -m black -S --line-length 79 .

isort:
	docker exec defi_pipeline isort .

pytest:
	docker exec defi_pipeline pytest /code/test

type:
	docker exec defi_pipeline mypy --ignore-missing-imports /code

lint: 
	docker exec defi_pipeline flake8 /code 

ci: isort format type lint pytest

stop-etl: 
	docker exec defi_pipeline service cron stop

####################################################################################################################
# Set up cloud infrastructure

tf-init:
	terraform -chdir=./terraform init

infra-up:
	terraform -chdir=./terraform apply

infra-down:
	terraform -chdir=./terraform destroy

infra-config:
	terraform -chdir=./terraform output

####################################################################################################################
# Datawarehouse migration

db-migration:
	@read -p "Enter migration name:" migration_name; docker exec defi_pipeline yoyo new ./migrations -m "$$migration_name"

warehouse-migration:
	docker exec defi_pipeline yoyo develop --no-config-file --database postgres://root:root@tokendb:5432/defi ./migrations

warehouse-rollback:
	docker exec defi_pipeline yoyo rollback --no-config-file --database postgres://root:root@tokendb:5432/defi ./migrations

####################################################################################################################
# Port forwarding to local machine

cloud-metabase:
	terraform -chdir=./terraform output -raw private_key > private_key.pem && chmod 600 private_key.pem && ssh -o "IdentitiesOnly yes" -i private_key.pem ubuntu@$$(terraform -chdir=./terraform output -raw ec2_public_dns) -N -f -L 3001:$$(terraform -chdir=./terraform output -raw ec2_public_dns):3000 && open http://localhost:3001 && rm private_key.pem

####################################################################################################################
# Helpers

ssh-ec2:
	terraform -chdir=./terraform output -raw private_key > private_key.pem && chmod 600 private_key.pem && ssh -o StrictHostKeyChecking=no -o IdentitiesOnly=yes -i private_key.pem ubuntu@$$(terraform -chdir=./terraform output -raw ec2_public_dns) && rm private_key.pem