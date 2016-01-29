if [ "$1" == "" ]; then
  echo "Usage: manage.sh COMMAND [arg...]"
  echo
  echo "Create and manage Docker instances for this project."
  echo
  echo "Commands:"
  echo -e "  configure\t\tCreate, start and deploy a new Docker instance."
  echo
elif [ "$1" == "configure" ]; then
  docker-machine create {{ cookiecutter.repo_name }} -d virtualbox
  docker-machine start {{ cookiecutter.repo_name }}
  eval "$(docker-machine env {{ cookiecutter.repo_name }})"
  docker-compose -f dev.yml build
  docker-compose -f dev.yml up -d

  echo "Django server should now be running at http://$(docker-machine ip {{ cookiecutter.repo_name }}):8000/"
  open "http://$(docker-machine ip {{ cookiecutter.repo_name }}):8000/"
else
  docker-compose -f dev.yml run django python manage.py "$@"
fi
