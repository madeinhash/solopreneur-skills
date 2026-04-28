FROM public.ecr.aws/docker/library/node:22.14.0

ENV TZ=UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Create app directory
WORKDIR /usr/src/app

# Install app dependencies
COPY package* ./
RUN npm i

# Bundle app source
COPY . .

EXPOSE 4000
CMD [ "npm", "run", "dev" ]
