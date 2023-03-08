#!/usr/bin/env ruby

cmd = ARGV[0]

def run_broker
  puts '* Starting RabbitMQ'

  puts `kubectl create -f https://raw.githubusercontent.com/kubernetes/kubernetes/release-1.3/examples/celery-rabbitmq/rabbitmq-service.yaml`
  puts `kubectl create -f https://raw.githubusercontent.com/kubernetes/kubernetes/release-1.3/examples/celery-rabbitmq/rabbitmq-controller.yaml`
end

def load_images
  puts '* Loading images into the kind default cluster'

  puts `kind load docker-image nokal/simod-queue-worker:0.0.0`
  puts `kind load docker-image nokal/simod-http:0.2.0`
end

def deploy
    puts '* Deploying the application'

    puts `kubectl apply -f deployment.yaml`
end

def port_forward
    puts '* Port forwarding'

    puts `kubectl port-forward deploy/simod-http :8000`
end

# kind create cluster --config kind-cluster.yaml

if cmd == ''
  load_images
  run_broker
  deploy
  port_forward
elsif cmd == 'broker'
  run_broker
elsif ['images', 'img', 'imgs', 'load_images'].include? cmd
  load_images
elsif cmd == 'deploy'
  deploy
elsif cmd == 'port_forward'
  port_forward
else
  puts 'Unknown command'
end
