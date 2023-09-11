# _L7 Homework #1_

I've used Django, Vue.js, and jQuery to build a single-page web application for this project.
You can get a clone of the project using the following commands
```
mkdir HW
cd HW
git clone https://github.com/imanm2001/L7.git
```
Run the web application using the following Docker's command
```
cd L7
docker compose up -d
```
and to stope the service use the following command
```
docker compose down
```
The web service will be run on port 8000. This port can be change by changing both `compose.yaml` and `Dockerfile`.

## _Create a new component_

Each component needs a Vue file for the front-end and a Python file for the back-end. These two files are linked together by linking the Python’s methods annotated with @webmethod() to Javascript. The Vue file should be stored inside files/js/components and the Python file should be stored inside classes. Both files should have the same name but different extensions.
## _Create a new applet_

Creating an applet is similar to a component with one difference. The class needs to be annotated using the @applet attribute.
```
@applet('componentName','Display Text,'path/to/img')
```
Since we are storing all of the images inside files/js/ the image path should be relative to this folder.
### _Web Methods_
Upon receiving a request to load a component, Django’s viewer will make a list of all functions annotated with @webmethod, and for each method, it attaches two methods, one with the same name, and the other one with “Async” added to the end of the name. Calling these methods in the front-end will invoke an Ajax call to the same method in the back-end. The result of the call will be returned to the front-end after stringing the returned object.
