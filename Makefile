# Makefile for honk docker IMAGE_NAME
# By: Fredrik Lundhag <f@mekk.com>
IMAGE_NAME := discord2elastic
DATA_DIR   := $(PWD)/config
DOCKER     := docker
HUB_USER   := $(USER)

.PHONY: run commit push

ifeq ($(VERSION),develop)
     ver=$("")
else
    ver=-r $(VERSION)
endif

build:
	test -n "$(VERSION)"  # test if version is set
	$(DOCKER) build --rm \
		--tag=$(IMAGE_NAME) \
		--tag=$(IMAGE_NAME):$(VERSION) .

run:
	-$(DOCKER) rm $(IMAGE_NAME) # remove the old container
	$(DOCKER) \
		run \
		-e ELASTICSEARCH_INDEX=${ELASTICSEARCH_INDEX} \
		-e ELASTICSEARCH_URL=${ELASTICSEARCH_URL} \
		-e BOT_TOKEN=${BOT_TOKEN} \
		--hostname=${IMAGE_NAME} \
		--name=${IMAGE_NAME} \
		$(IMAGE_NAME)

stop:
	$(DOCKER) \
		kill ${IMAGE_NAME}

history:
	$(DOCKER) \
		history ${IMAGE_NAME}

clean:
	-$(DOCKER) rmi --force $(IMAGE_NAME)
	-$(DOCKER) rmi --force $(HUB_USER)/$(IMAGE_NAME)

push:
	$(DOCKER) tag $(IMAGE_NAME) $(HUB_USER)/$(IMAGE_NAME):$(VERSION) && \
	$(DOCKER) tag ${IMAGE_NAME} ${HUB_USER}/${IMAGE_NAME}:latest && \
	$(DOCKER) push $(HUB_USER)/$(IMAGE_NAME):$(VERSION) && \
	$(DOCKER) push ${HUB_USER}/${IMAGE_NAME}:latest

commit:
	$(DOCKER) commit -m "Built version ${TAG}" -a "${USER}" ${IMAGE_NAME} ${HUB_USER}/${IMAGE_NAME}:${TAG}
