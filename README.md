# Neuraphonic

## Inspiration
Diagnoses for mental health disorders are riddled with delays, high costs, and un-intuitive instructions for people that are most vulnerable. Specifically, we've found that Parkinson's Disease diagnoses are highly expensive and lengthy, and may not always be necessary for everyone who fears that they have Parkinson's Disease. Furthermore, GP centers in the US and EU have been backed up due to many patients' speculation on having Parkinson's. Thus, we build Neuraphonic to act as a middleman on the road to Parkinson's Diagnosis; it can serve as a first test to see if a patient should seek further testing for Parkinson's Disease.

## What it does
Neuraphonic is an audio sample based Parkinson's Disease symptom predictor. The system is sent an audio sample via phone call or web upload, and the custom-built two staged audio processing pipeline interprets the audio signal and detects features in the signal that may signify Parkinson's Disease.

## How we built it
The core of Neuraphonic's web interface is a Flask application deployed on Google Cloud and hosted via .tech's hosting service. The Flask application has a record and upload interface to allow the user to record a voice sample, or upload one of their own. Once the voice sample is recorded it is sent to the execution pipeline, which contains a signal processing pipeline and an ensemble model. 

The signal processing pipeline decomposes the audio file into an image representation, as well as a tabular representation of its key features and metrics. The signal processing pipeline was prototyped in MATLAB, and was later deployed using the Praat Algorithm in Python. 

The image and the tabular representation are sent into the ensemble model, that sends the image into a fine-tuned Vision Transformer (ViT) model, and the tabular representation into a Random Forest. The two models execute independently, and their results are probabilistically interpolated and sent as a majority-rules vote. The Flask application receives the response via an HTTP endpoint, and formats it into a user-friendly format, which is displayed to the user, along with actionable feedback. 

The model is stored in a Google Cloud Storage bucket, which is a long-term persistent storage region to store the pre-trained Vision Transformer and Random Forest model.

To allow for greater accessibility for patients, we implemented phone-call API through the Twilio API. This allows for patients to call a specified phone number and have their voice be recorded and told over audio whether there was a high-likelihood of having parkinson's disease, requiring a visit to a medical center for further neurological tests. The Twilio API is done through attaching webhooks to our webapp and linking it to a specified Twilio phone number. Once the phone number is called, the twilio webhooks execute, record the audio, and then run it through our ML model to get the final results for the patient.

## Challenges we ran into
One of the biggest challenges we ran into was deploying the system on Google Cloud, as its storage and compute limitations were rather significant, thus we had to rework the way we trained, stored, and executed the machine learning models to ensure they could fit in Google Cloud's limitations. These limitations were significantly outweighed by the benefits of Google Cloud, which included the ability to universally deploy our model.

## Accomplishments that we're proud of
We had three major accomplishments that we were proud of: training a Vision Transformer completely, implementing various famous Signal Processing algorithms by hand, and successfully deploying the model to Google Cloud and having it universally work. These were three major challenges that had troubled us in previous projects, and overcoming these difficulties was very satisfying. 

## What we learned
This project involved a wide variety of technologies that we had minimal to no experience in, including signal processing algorithms in python, Transformers, Google Cloud deploying, security, and backend routing.

## What's next for Neuraphonic
1. Establish a way to connect to the interface via a phone call: a user could call in and send a recording and have a phone API sent the recording over to the execution pipeline.
2. Establish an SSL certificate so that the Neuraphonic website uses HTTPS instead of HTTP. Once established, the user can record their voice in real time and send their voice for processing instead of pre-recording a file.
3. Our datasets are comparatively small for the sheer size of the models, and because we only had 36 hours on limited hardware, we could not train the model to the extent we desired. With more time, we would significantly optimize the models and perhaps use it for multi-class classification.