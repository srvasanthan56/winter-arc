An app has a base language it is written and its libraries , database , other services and environment variables, lets say a Project running in Node JS will run only in Node 16 , but at the same time another project has Node 20 , so its much of a hassle to switch between different node versions , and 
Before Containers to run a app, we had two ways one is setting up a *Bare Metal* and *VM*
- It keeps isolated environment without the VM overhead
- Fast, Cheap and Disposable, ligthweight
- Image is lightweight and universal 

The same image runs identically on my laptop , teamates, EC2, and production server, No More "works on my machine"

in pandas version < 2.0
df.append works fine, but on pandas version 2+
it fails ,


## Getting Started

### Creating a linux container with volume
 nerdctl run --rm `
 -v "D:/docker-volumes:/test"`
 alpine ls -la /test

