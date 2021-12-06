## Background

I just finished creating a few small lambda functions using Python.
Layers are a great way to manage application dependencies, and speeding up your deployment times.

My project needed the following libraries:
* [`requests`](https://docs.python-requests.org/en/latest/) for making HTTP requests.
* [`pysftp`](https://pysftp.readthedocs.io/en/release_0.2.9/) for creating SSH connections to different servers. 

If you need a different library, the approach should be the same, assuming it's installable using `pip` or `pip3`. 

Unfortunately we didn’t have access to [Container Registry (ECR)](https://aws.amazon.com/ecr/) so we couldn't create a docker container, which would have allowed us to install the dependencies as part of the docker container creation.

We instead had to create & upload a zip file containing our application code and dependencies.
 
While we could include the application dependencies in the zip we upload, this has a few disadvantages:
1. It slows down each upload, which is not ideal as you might end up uploading a number of times. 
2. Your application code will not be viewable in the lambda console if your zip file ends up too large.

## Creating a AWS Lambda layer

### Application Setup

So now we know why layers might be needed in your lambda function, let's look at how to create one.

Folder structure of a lambda layer: 

```
/requirements.txt
/python/
```

Where `requirements.txt` is a file with the names of the packages we’re using, and `python` is an empty folder which we will be installing dependencies into. See the [Lambda layer documentation](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html) for more information on why we need to install into the python folder.  

My application folder on my computer looks something like this then:
``` 
/lambda_function.py
/lambda_layer/requirements.txt
/lambda_layer/python/
```

### Setup Ubuntu VM 

AWS Lambda runs in a Linux machine, so you'll need to install the layer dependencies using an Linux OS. You can't directly follow these steps in MacOS or Windows.

I won't cover how to create a Linux VM, as there are many good tutorials available with a quick search online.

### Create the layer ZIP file

> Remember, you need to run these commands in a Linux machine.

Navigate into the layer folder:
`cd lambda_layer` 

Install the dependencies into the python folder:
`pip install -r requirements.txt -t .python`

Create the lambda layer zip:
`zip -r ../app-name-depts-layer.zip *` 

We now have a ZIP file (`app-name-depts-layer.zip`) which can be uploaded to AWS as a Layer. This zip file should have a python folder inside it, with the application dependencies installed from `pip` inside.

## Create the layer in AWS

Navigate to your AWS instance, and open Lambda function. Click the create layer button:
￼
![AWS Lambda create layer step 1](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/rxboyif8rtwkmcy5n0cm.png)

Fill in the details of your layer:

> I recommend including the names of the packages that are included in the layer, as part of the description. This will be useful in the future, especially if you end up creating and using multiple layers.

￼![AWS Lambda create layer step 2](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/1uhaetulsxvo64ppo0hb.png)

Click _Create layer_

## Configure Lambda function to use Layer.

In your lambda function, scroll down to the bottom of the page, to the Layers section: 

Click on the _Add a layer_ button

![Add a layer to AWS Lambda function, step 1](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/85h5tltm0qvik3a9lbse.png)

Select _Custom layers_, then select the layer you just created, picking the latest version:
![Adding a layer to an AWS function](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/dtn4hxk80ksnx6yet3wx.png) 

Wait for the function to update:
![AWS Lambda function updated after adding layer](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/qrgmwii4o7nmnwdbtr4y.png)

That’s it! 

## Test it out

Now in your application code, you can simply import the packages installed in the layer. 

**`lambda_function.py`**
```
import requests

def lambda_handler(event, context):
    test_url = 'https://jsonplaceholder.typicode.com/todos/1'
    response = requests.get(test_url)
    
    return {
        'statusCode': response.status_code,
        'body': response.json()
    }
```

In the console it should look like this:
![Screenshot of AWS console - showing test Lambda function](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/zxfv0996jqqnsfzs2u2v.png)

Testing this code should return: 
![Result of test using application dependency from layer](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/8jipadodw1yh9h0e126l.png)

You now have the ability to make HTTP requests and can easily reuse the layer in different applications.

Hopefully this is enough to get you started, you can easily extend this out as needed...
