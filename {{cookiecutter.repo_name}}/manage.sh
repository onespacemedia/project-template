if [ "$1" == "" ]; then
  echo "Usage: manage.sh COMMAND [arg...]"
  echo
  echo "Create and manage Docker instances for this project."
  echo
  echo "Commands:"
  echo -e "  configure\t\t\tCreate, start and deploy a new Docker instance."
  echo -e "  <manage.py subcommand>\tRun a manage.py subcommand on the Docker instance (e.g. migrate, createsuperuser)."
  echo
elif [ "$1" == "configure" ]; then
  docker-machine create dev -d virtualbox
  docker-machine start dev
  eval "$(docker-machine env dev)"
  docker stop $(docker ps -aq)
  docker rm $(docker ps -aq)
  docker-compose -f dev.yml build

  echo "Django server should now be running at http://$(docker-machine ip dev):8000/"
  docker-compose -f dev.yml up -d
else
  docker-machine start dev
  eval "$(docker-machine env dev)"
  docker-compose -f dev.yml run django python manage.py "$@"
fi
