
if [[ $# != 1 ]]; then
  echo "usage ./docker.sh <docker_image_name>"
  echo "ex :- ./docker.sh nginx"
  exit 1
fi

echo "Setting docker workprofile"
cp -r ../roles/ ../dockerDistb/
cp ../main.yml ../dockerDistb/
sed -i -e "s+hosts: nginx+hosts: localhost+g" ../dockerDistb/main.yml
echo "Copy completed"


echo "Generating Docker build"
docker build -t $1 .

if [[ $? == 0 ]]; then
  echo "Docker build generated successfully"
else
  echo "Docker build failed"
fi
