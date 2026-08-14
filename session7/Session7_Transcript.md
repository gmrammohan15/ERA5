## **ERA V5 Session \- 2026/08/08 06:43 IST \- Transcript**

# **Transcript**

The Admin: This is exactly one was in tokenizer the other was in the emitting layer and I leave you with some questions where you can think and decide do you have some ideas where you can also contribute and actually write a paper so yeah first opportunity now we're going to talk about embeddings and model internals in the last six sessions we focused on deciding what kind of data we want to collect how do we collect it how do we for instance clean it up how do we dduplicate

The Admin: that and about fertility all of those concepts are going to be coming in today and you'll start to feel there's a much tighter integration between the data and the model that we train both are not isolated and the direct effect is going to be on the embedding side right so I hope you really enjoy this so as I was saying the data part is finished now so how do we collect we have not written the code for that there are a lot of good ideas in the assignment that you have submitted so they are going to be taken back into

The Admin: the main code and we are going to run that. We still need to decide how do we divide the teams and make you work on collecting the data part. But the data side is sort of done. Next five six sessions are going to be mostly on understanding the neural network the transformer how does it work from being a small model to a big model what are the differences or what are the choices we have if you go with a small model or a big model. In fact one of the re revelation is going to be today itself. when we ended the session two we said the tokenizer job is complete the moment the text has become a sequence of integer.

The Admin: Rest of the sessions were to figure out how do we get the best text but till that time we just knew that we have a token that converts into a integer somehow right now that integer is going to go inside our model and that's where the first conversion is going to happen which is converting this token or integer into something that ural network can digest or neural network can believe on or rely on or improve on right that's where the session is going to be which is what the embedding layer is now what you need to realize is when we created our braic tokenizer this is a tokenizer that we made in V4 this year we're going to be making a new one we have a vocabulary of 131072 tokens which means that first of all tokens if you have forgotten they are subwords so pre-eposition so pre is

The Admin: token deposition the tok to token because both might be used in many other places also sometimes the whole word becomes a token like India because we see it a lot so we run an algorithm and we figure out what is a candidate for our token vocabulary right and that sits inside our bucket so that we had 131072 why that number we're going to see you'll also realize yourself that it's a good number of 2 to power plus few things right now that's a token right

The Admin: These are tot number tokens we have. But when we feed it into the model, each token becomes something like 96 dimensions. Sorry for that. Each of the token becomes 8096 what are embeddings? Again in last few sessions we've discussed these are places or vector spaces which define everything. For example, a 3D point has three dimensions, right? So, we'll call a vector point has a 3D vector point has three embedding dimensions. The better way to say because we have one 310 72 tokens and these are the embeddings and the embedding dimensions 096\. Right? So, a 3D point can be determined in three axis. But if you had time then becomes fourth axis.

The Admin: But if you add for example velocity also to a point then we have made 3 \+ 3 \+ 1 right so now we have seven what if we add acceleration also so we have 3 3 9 \+ 1 10 okay but what about angular momentum okay so three more so 3 \+ 3 \+ 3 so you understand right as the dimensions are increasing we are able to add more data about a particular point right we have angular momentum we have angular angular acceleration as well. then we can add vorticity as well for that particular point or we can add energy for that particular point. Moment we say energy then there's at that point what is the electrical current in all the three axises. Then we have magnetism gravity we have mass So you can imagine a point which can just be decided by three things is the least minimum informment for Just telling us I am at XYZ.

The Admin: But if you want to add more data to what that point actually is, then you can keep on adding more and A point on a 3D map of a globe can tell you far more. Right? It has a longitude, latitude, it has its own XYZ in the universe. Then that same point has a population. The same point may have a cost per square feet. If it is in Indranagar, if it is in Delhi, if it is in the middle, so it has a price also. So these dimensions are telling us something very specific and each dimensions is locked. So first dimension may be for whether a person is a gender male or female. And maybe the person is rich or poor

### 00:05:00

The Admin: Third maybe it's a person or not. The fourth maybe does it have a relationship with let's say electronics or electrical or mechanical. before 2012 there was a field called feature engineering and most of the humans or people who were saying that we are working in state-of-the-art machine learning or computers or computer vision they were doing feature engineering which meant that these people had to sit and figure out these dimensions for different things. problem of humans is that you cannot think out of the box right some can but for every single problem we can't and the reason is that we have to think for a problem very hard and then we can come back with a very very beautiful solution and that is a PhD but we needed this breakthrough for every single feature now we don't cover convolution neural networks but I'll definitely like to share an example straight away and question goes to you detecting a circle is one of

The Admin: very important problems in computer vision especially in manufacturing where we need to count number of things writing a kernel for that a kernel is something that looks at an image and we so imagine a kernel is like your blackboard duster and you have a big u blackboard and you're just rubbing on top that's a kernel so the duster in your hand is a kernel that sweeps across the whole image and tries and finds something the way it finds it wherever it is it will multiply its own value with what it's searching for and we will get a peak if it does find so kernel is literally a meth

The Admin: matical matrix that is looking at a way bigger matrix but it just scans it step by step. So if you find a circle this kernel is going to peak. So now we have The problem is that what is the radius of the circle because it's You cannot have small kernel that identifies a identify big circle. What if the circle is not a circle? It's an ellipse and what if it's not a x ellipse or it's a y ellipse? What if it is squished right? What if it's actually not a finished circle?

The Admin: because sometimes occlusion might also happen. what do you think what kind of kernel you will come up with? Because now I will show you what neural networks come up with. Anyone? If you have done U E Va then Bali you definitely know Chatali also knows Can I ask the question again?

Balaji Chunduri: Can you ask that question?

The Admin: Good morning.

Chaitali Debp: A good body.

The Admin: The question is before 2012 we had a problem that So to identify a circle we have to make a kernel that can go on top. Let's say this is a screen and we have a circle here.

The Admin: So we'll make a small kernel that is going to move around here and here and here and here and here. So if it comes on top of it, it's going to say yes. I found a circle right but the problem is what is the dimension of the circle it can be many what if the circle is not a circle but it's actually oval like this and what if it's not finished so the question to you is what one kernel will you come up with as a human which can identify all of these and this example is actually going to tell you that what AI is actually doing in the back end what do you think what kind of kernel this will

Balaji Chunduri: So it'll be something that can learn from the features.

The Admin: I want you to tell me…

The Admin: how does it look or how will it find all of these variants and…

Sachin Bharadwaj: It's an average of everything what

The Admin: everything is just going to be a blur image.

Chaitali Debp: The three cross

The Admin: Yeah. 3 \+ 3 what does it do? Yeah. Location is the answer. Hey, don't talk MBA,…

Balaji Chunduri: Just learn features like smaller edges or…

Balaji Chunduri: those low-level features.

The Admin: talk engineering. So, the answer is what Lo said. It's going to be a spiral. And I hope I find it for you. It's definitely in the Good.

Chaitali Debp: It looks in the center pixel and then surroundingly with the others and then a checkerboard it is going to go and identify Yeah.

The Admin: You're doing MBA. V1 should have it.

The Admin: Yes. Where is receptive field?

The Admin: Yes. Receptive field it.

Satyanarayana Murthy Toleti: If it…

Satyanarayana Murthy Toleti: if it looks at the edges, it may become

### 00:10:00

The Admin: No ma'am. The moment you see you will realize. I hope I find This used to be EVA course. So I'll have to go to EVA code or EVA for 100% should be perceptive field and new unit works. There's so much of science that I can't even tell you. I just hit myself also for that. Yeah, here it is. Right. So, it comes up with this kind of kernel. s A spiral has all the shapes of a circles. A A spiral has ellipse in all the directions.

The Admin: And it's really impossible if you don't see what neural networks learn to be able to understand why they work in a way they do. And the reason that they can come up with something like this is because they can look at the image millions of times and billions of times in different areas,…

The Admin: different reasons. And we tell them that you have to come up with only one kernel for doing all of that.

Chaitali Debp: I remember that convolutional kernel from…

Chaitali Debp: where we get the convolutional neural network that is a 3 \+ 3 grid in a receptive field that refers to the 3 \+3 area of the input image and…

Chaitali Debp: the neuron can see it and then gradually convolutes.

The Admin: Yeah, I've given the answer already.

The Admin: So, don't break the flow, please. So this is our new

The Admin: networks too, right? and that is something that is coming from looking at billions of data. why is it linked to what we are talking about here? I just mentioned that we are going to have 8096 dimensions. you might immediately start thinking and this thought is early 2012 or before 2012 is What is the meaning of third dimension? Do I I want to know what is the meaning of 14th dimension? And Why not 16,000 dimensions? This is as good as me asking you what are you going to store in the first dimension. You're going to say gender. What you realize immediately is that you have exactly the same problem what we had in circle. What is a Male, female and then you have multiple other kinds also. There are animals that change the gender based on the requirement. There are fishes that do that. How do you define all of that? When we say a word like transaction, how many kind of transaction can we incorporate with that particular feature? We can't think humans are sort of deterministic.

The Admin: We know a few feelings and other things but based on what we are feeling the meaning of word also changes right a red might be a beautiful word on let's say Christmas or valent valentine but in hospital red is not a great word to look at and a neural network can look at all of those dimensions or all of those requirement and come up with something that has literally no meaning for us and that is what it is going to find and put in this 8096 we can try and figure out that for example in the dimension number 14\. So we have 8096 again something we'll see at the bottom also. But let's say we have 8096 number for each of our token. Let's start from scratch. We have English word or Hindi word. Sometimes it will be used as a whole India. Sometimes it may not be used as a whole for example prede In that case we'll divide into pre-indeposition. Right? but both of these word together will mean something in the neural network.

The Admin: Let's say we're saying When the India word is sent to the new network, how do we send it? India will have an ID that is a index number in the whole table that we have built for our vocabulary. Let's say that that ID is So 11,000 cannot enter new network. 11,000 has to convert into these 8096 numbers. And these 8096 numbers are going to be sent to the new network. And these 8096 number for every single word that we have will define what this word means. Are we clear till here? this part is very important because we're clear till here then I can move forward because rest of the session is talking about what these how do we work with it what is the cost of deciding that number and blah blah blah any question till now 100% this is everything

NITIN YADAV: So Rohan the number like this size 8096 or less or more than that can this drive how the model performs?

The Admin: Because this is like a bandwidth.

NITIN YADAV: Okay. No.

The Admin: The perfect way to understand this is a bandwidth. We looking at 8 Mbps right now, Every single word has eight or nine ways of describing itself. If you had 16,000, then you're suddenly doubled it. So each meaning can have a multiple. For example, how many colors do you know? Are you married? You're not married. You have a girlfriend.

NITIN YADAV: Yeah. Yeah.

The Admin: How many colors do you know versus your girlfriend?

NITIN YADAV: There is a difference.

The Admin: There's a difference because your embedding is poor probably 20\. Her embedding is 20,000.

The Admin: Women can understand 20,000 different colors, right?

The Admin: And that's precisely the meaning of what these embedding dimensions are doing. How detail can we talk about something? For example, apple has three meanings that we can immediately think of. One is the fruit that we eat. Second is going to be the apple as a company and third we use for kids like an apple of my eye, right? so each word can have multiple meanings. It has to store it because before we send it to neural network the word is going to be a self containing meaning in every single possibility. Bank for example is my favorite word. Bank is a financial institution. Bank also means the corner of a river. Bank also means that angle that we give to a road when we are taking a speed The three meanings there also. So it has to store everything. The moment again we say Apple of course as a electronics company but inside it will have relationship with phones with electronics with Steve Job with entrepreneurship with design and…

NITIN YADAV: Mhm. Hey

### 00:15:00

The Admin: a stuff.

The Admin: So whatever a word emulates a feeling in every single context must be stored in 8096\. Can you imagine how much work is required to do to get the right 8096 and if you reduce it to 1024 suddenly we have said you have only 1/8 the bandwidth. So we can only store this much.

NITIN YADAV: And you mentioned that earlier we supposed to do feature engineering,…

NITIN YADAV: right? But somehow we need engineering to decide the the importance of each of the dimension of this embedding right now also.

The Admin: No no no no no no before 2012 we thought we could do it and we were doing it that is when the AI came in now we can't compete…

NITIN YADAV: So as a whole Okay.

The Admin: because of the circle thing I showed you that we cannot just think new networks because they can look at an example millions of times humans can't for every single problem we just say right now that dude I'm giving you 8 Mbps or…

NITIN YADAV: Okay. Thank you.

The Admin: 16 MBS or 1 MBS

The Admin: I'm a poor person. So 5 MPS exactly…

Pratik Mukherjee: So that 8096 is basic basically come I mean why we choose 8096 comes down to the amount of money we have or what is the Okay.

The Admin: if you take the right word amount of money everything is money right and we'll see it has cost and there is a bit of science also that says that you cannot go beyond this or below this for a particular kind of model. So there are papers that refer to that but for us it's slightly different and we'll discuss why but it is more or less linked to the amount of money we have. Okay. But the problem is if I take

The Admin: 131072 and multiply that by 8096, we get a billion parameters. So the moment you decide your vocabulary is 131,72 and each one of them has 8096 embeddings. We're talking about a billion parameter and you need to know today and we're going to go deeper also a parameter that is trainable has 16 bytes of data that is required to be saved for that stored for that when we are so it's not one so you're not looking 1 billion you're looking at around 8 GB of RAM being used for this model and batch one moment you say we have a batch of 100 examples there you go right so this is going to expand a lot but still let's

The Admin: start with that. one building parameter is going to be around 2GB of just the bytes in the BF14. We're going to talk about what is a BF14. you may have heard of float 32 is that we can store 32 positions of and basically again bandwidth. How much detailed number Can we save 0.01 2 3 4 5 6 7 8 9 very small number. And then we have floating 16 where we have a lesser precision. And then we have BF16 is brain float 16\. It was invented by Deep Mind. the guy who got Nobel Prize in chemistry. Dennis Havis, he was one of the author of this particular paper. We're going to talk about what this is. This is slightly interesting. This has more range but less depth. Something like that. But we'll talk about what it means later on. Right. So in BF16 also it's going to take somewhere around 2.12GB just to mention the parameters.

The Admin: We're not even talking about training parameters or the atom which is optimizer the states that we're going to save. By the what you need to reme remember and slowly build your intuition on and we will go deeper in that particular topic today is when we talk about a parameter especially in case of u u transformers we have not discussed convolutions. So what I'm saying is true for all the models because transformer all the models for us every single parameter when we train it the training means that we initialize it to some random value like 34 but maybe the final value should be.13.

The Admin: So the journey from 34 to.13 is the training. It's going to look at example back propagation. The king of fixing all the weights is going to see that this weight is not at the right position. Let me move it and see moving in this direction loss reduces a bit. Right? So it's going to change that and next time it comes in is again going to change that. Now the problem is and I could have shown it to you. I can't show it to you. So the problem is if you just change it based on data, the current data may be biased in a single direction and you might lose all the things that.

### 00:20:00

The Admin: I think for example in a movie let's say Yi decided Apple is going to be a replacement for MCBC just for a moment and then we call someone an apple and this piece of data goes inside the neural network and your network learns it suddenly whatever has learned about Apple is going to turn around and going to start looking at the slangs that we use so one example is good enough to destroy what we've learned right so one example is not good enough for us to be confident that this is the direction we need to go. So we're going to store a lot of different things. We're going to store in fact let me not answer that. Let me ask you because this intuitional knowledge is important. and it's very similar to how a heat seeeking missile should work. So this is where our missile was and this is where our moving object was. Okay. What will you do? How will you write this algorithm?

The Admin: We need to track and kill that guy. So let's say that we know the and the location happens to be here. So we draw a vertex and go in the direction. Is this a good algorithm?

Sanjay Kumar: Nope. I think we should look a bit forward than what we are targeting at I feel

The Admin: Let's define that also. meaning of looking a bit forward was that I knew the target was here. I looked at a delta D and we have world's best radar and other systems and based on that I predict that it's going to be here and instead of targeting here we target here. Is this a good algorithm?

Dattatreya Manjunath: It's better to keep iterating over …

Suresh Mantha: We need speed of both of them.

Dattatreya Manjunath: how it's moving and…

Dattatreya Manjunath: then change the direction accordingly in direct.

The Admin: Yeah. No,…

The Admin: tell me explain on the screen because just using words not to explain is not MBA speed.

Dattatreya Manjunath: 

Dattatreya Manjunath: Okay. Okay. Yeah. So,

The Admin: Let's say this I'm drawing let's say relative. So let me ease that down. So let me go slightly technical. This was the first order. You have just done second order. The problem is what if the particle or object was like this, right?

The Admin: And it's actually making this kind of turn that means that I should have taken this order also. So first is called distance or you can say displacement then we have velocity then we have acceleration and then we have impulse the rate of change of acceleration and there is no stopping you can go and everything has to be smooth right certainly you can't have and radars and other stuff just like how we are going to see are not accurate. I don't know if you have ever seen object detector radar is very similar to object detector. So there's a car sometimes it's going to show you a bonding box like this. Then Sometimes it will show you like that. And then converting that into a point is going to be a nightmare because you're going to get a speed which is changing very very fast and very very slow.

The Admin: So not only we need to take the distance, we need to take the velocity, the acceleration and the momentum also, right? We need to conserve the angular momentum, we need to conserve the acceleration. So once you add all of that, then you have relatively good tracker. Same goes for our parameter. It changes in the class.

Chaitali Debp: So also the x y and z position right the vertical position is horizontal.

The Admin: You need to raise the hand then you need to let him stop and So we need to maintain the velocity the acceleration the impulse also right and all that data is exactly what we are going to do for our parameter also because our parameter is here our back propagation comes in and say dude you need to be here and then next time it comes and say dude you need to be here then next time it comes and say dude you need to be here and here and if you fluctuate it that much neural network will take a very long time to stabilize that's why we do something exactly what we do here this algorithm for our new network is called Adam and you're going to

The Admin: Here are a lot of different flavors for this. We have Adam, we have RMS prop, we have L delta, we have SGD which we don't use in transformers but all of these are different slightly variants of this algorithm. moment you see this graph also you're going to see that okay this looks like vector. So if I take this and take that I would have gone there. If I take this and this and this I would have gone there. we try and ease down. We decided okay this whole thing doesn't make sense. So let me only take 90% of it. So how much of history we take how much of future thing if you ever worked in stock market then this thing called EMA right weighted means so we take a weighted mean of what is the new information coming in right for example if I ask you that the FC stock has dropped down by 20%.

### 00:25:00

The Admin: Does that define the company today watch but you get the idea. A stock change just for a moment I don't know any of you are aware of SDFC what is happening there but a momentary change in something does not reflect its own behavior since the perpetual history we have had. So those are the things that we're going to be looking at so there are five things that we need to understand and this is the scene.

The Admin: This is where the tokens are going to be fed to the model. So here you're looking at what part connects with token ids. Do you remember What is a token ID? So once we make our tokenizer and convert all the text, we have this token vap. So let's say we have only four tokens just to keep my life So token is going The second important token is going to be getting let's say the first token is and then B and C and D and okay sorry again I'm doing a mistake which will confuse you. So let's say it's going to be D E C A and B right the order can be anything. So the token ID here

The Admin: is let me start with one and then two and then three and then four and five. Right? if we had 1 3 1 072 tokens that means those are the numbers of ID we have. So last token would have had 13 1 ID that is the Clear on that so every token we have will have an ID the number in the list where exactly it's sitting. We discussed and if you have forgotten then go back to last session. We discussed that we will try and make our tokenizer in such a way that if the token ID is 45,000 and if the token ID is 100,000 we know 100,000 occurs less in our data set compared to 45,000. We'll try and make a tokenizer like that because we want this ID to be representative of something else also. We have again the same concept. We're fusing more data into the single points we have.

The Admin: So we can use that later on and In fact, today you'll also need know why it is important. So we're going to take our token ID. let's say there's a word called the sun is rising. So the first thing we're going to do is to go inside our vocab and see what is the ID of the I'm going to use smaller numbers here so we can remember them. 97 103 and let's say 46 exclamation is also there. So we have to have a token for that. here let's say exclamation will come a lot. So let's say 13\. Right? These are imaginary token ids that I have made. Are we clear on this? So in this token id in 64 that t represents that and why in 64 because it needs to represent all the tokens we have.

The Admin: N64 gives us enough bandwidth to be able to store them. You can come back and say no I can represent them in some other lesser integers also. You can but that is what we have when we train. So you can use a smaller part of a big bus. you can transport four people in a big bus that can travel 100 people but the bus has to move. mathematically and on GPU when we train this is the restriction we have. So that's why it's going to be in 64\. But then we have this Batch would mean that I'm not sending the sun is rising alone. I'm also going to send the moon is beautiful and an exclamation mark. And then I'm also going to send car went to the room or showroom. Right. How many batches do we see on the screen? Three.

The Admin: And we can have how many batches is decided by what?

Sachin Bharadwaj: Memory of this.

The Admin: Anyone? Money.

Rishikesh Kumar: Money.

Sagar pallai: Morning.

The Admin: Money does matter. So how many batches are going to be decided by money? And why money? because depending on the GPU that we have taken for training we have enough RAM and that RAM is going to determine what is the batch size we want the biggest batch size possible and we discussed that we like to target a 1 million token in each batch as we're sending it so here on our screen we have a batch size that is equal to three and we have 1 2 3 4 5 as token here right this t that we're talking about is going to be the sequence length what is the length of examples on which I'm training my neural network right now so we are going to start with 4k then move to 8k then

The Admin: we have 16 and 32 and 128 and so on. So that's the token ID and that is the system that we're going to be token ID here is going to be consumed by the embedding table. We going to talk about what this embedding table is. But you can immediately see B and T. B is batch. So just remember we have 4,000 of them and forget about it. So B moment you remove B from here the life is going to be slightly easy. So we are sending T tokens. How many? Five of them or 1024 of them. and that goes inside a embedding table is going to consume the token ID. Then we ID is going to be decided by a position policy. Now A comes before B. know I can write it down, And let me write it down and this is again important thing which you need to remember. Hello. Let's pick this.

### 00:30:00

The Admin: So Is this Does A come before B? Yes or no? On the screen,…

Varshith Chennuru: Maybe minority.

Raj H: Yes.

The Admin: does it on the screen? It does. But unfortunately, this is not how we feed to a network. How do you feed to a new network all at the same time? And that becomes a problem. The whole sentence and doesn't matter the length 4,000 tokens or two tokens or 5,000 tokens all are fed at once. And if you look at the math, it's in such a way that doesn't matter what you send where the algorithm is exactly same.

The Admin: Which means new networks internally do not have inherent way of understanding what is left, what is right. Everything comes at the same time. So for a new network it comes like this. Are we clear? Don't agree with me? Just look at this example. We have seen this earlier also. Right? These are the weights that we have and this is the data that is going in. and B goes in and this becomes 0.1 and this becomes 0.2. There's no way to figure out that A has to go from here and B has to go from here because math inside is deterministic.

The Admin: So that's a problem for us. So we can't do it. So the solution for this is very simple. We say A comes before B and we also send 0 1 2 and 3\. s. We have to send the position ID of the token when we are sending the tokens. Now you also get the position By the way, you live in time. So as you wait you can see that there's a word that comes after the word I'm saying and then before the word there are few other words also.

The Admin: So time is already giving us a perception of the forward movement right neural networks does not have the perception of forward movement and that is why we have to give the 0 1 2 3 4 so understand this is how the things are moving right so that's the position ID and we're going to spend some time on position ID today so don't worry on that so position ID will be decided by the position policy there are many different ways in which we can add this position and many different locations in which we can add this position so we need to discuss a bit about that today then we have something called a loss mask if you have done your prior assignments know what would it mean?

The Admin: So we discussed that when we are in the training and I'm sending the sun rises in the east right if this is pre-training then the loss will be calculated on each of the word yes no…

Abishek Ajai Satnur: Yes.

The Admin: but if you are in the QNA part in that cases the loss will not be calculated in these parts correct the loss will only be for east. You remember that also. So depending on the stage where we are, we're going to decide where exactly is the loss will be calculated and that is a loss mask. It's very similar to our tokens 0 1 2 3 4 5 6 but for zero we're don't force few we're going to say yes for few we're going to say no and so on.

The Admin: So that's a loss mask that will also be there and we need to prepare that while we preparing our data set for the data set which will go to let's say L or post training. Then we have mixture lane and stages. This is not something that goes inside the model but this is something that we need to know the metadata that this is a mix of indic or this is a mix of coding data or this is a matical data and what stage are we in are we in the 20 billion stage or we are in the early stage of training or in an stages right and then we have ledger tags what run we are on what stage we are on what step we are on or what is shard id shard is the bigger holder of the batch we have right so these are different things that come together but the most important three are token

### 00:35:00

The Admin: The position ID and the loss mask that we have now the loss mask and operate this I already explained so okay any question till now all right good so this is something that we don't know unless we are told about it and the lookup is gather and pometics multiplier. Generally, if you have never heard of new networks and transformers, then you're not confused. But if you have read outside how the embedding layer actually works, people think of something weird is happening with embedding layer. So, we're talking about the embedding layer and even before we do that, let's look at a transform architecture and I'm hoping we'll get somebody to Yes, you see this outp embedding. This is the embedding layer we're talking about.

The Admin: It is called embedding literally in PyTor also. So you're going to look at that. almost every explanation of embedding layer describes a matrix multiplication against one hot vector. And that description is mathematically true but operationally misleading. Everywhere you're going to find online that people say that how do we find embedding of a particular ID. We say that we take the whole embedding table which means 131 072 into 8,000. And I'm going to take a one hot vector. Do you know what is one hot vector?

Nikhil Shrimali: It's like a sparse matrix.

The Admin: This is a one hot vector, right? So we have one hot position to determine what is one hot one hot position to determine what is C and one hot for D, right? This is one hot vector basically one one and every thing else is zero and the location of that thing defines what is A. So to find embedding this is the description that is there online which I don't want you to even remember or look at what I wanted to know is that how does embedding look like because it's a big table we have 131072 and we have 8 096 of that and so let's say I need to get a particular number from that right so the operation that we use there is something called a gather which is we're just going to pick it up it's just a read you're not going to read the whole table like that's why we have ID also

The Admin: So it's like a dictionary pick you can search for it. We not going to multiply anything. So if you're not even confused then this sounds like okay this is just like a memory read. So it's not multiplication or not and that's all you're supposed to know. So doesn't matter what is If embedding table has 1 million tokens reading a single token out of that is free and cheap because we just doing a memory read. There's no mathematics involved online. If you search about it people are going to say that we are doing this multiplication and all. Not true on the computer. that does not happen. You clear on this? why is it important? So, what have we said? We have said that we have 13 1 072 rows.

The Admin: These are 131072 rows. You can count them. And when we get let's say token number 47, you just go to row number 47 and pick it up and drag it here. If you go for a token ID 1 3 0 4, we go to that particular row. Take it up and drag it here. Right? We just take it out and we just keep it at the location where we are sending. So this is exactly the sun rises and so on right those are tokens that we are pulling out and we are keeping at this particular location. So this is the gather part where we are just picking them and storing them. But what happens at the same time is this is going to be in the memory. Of course it has to be in the memory which means that when we're gathering I need to remember what I gathered. I'm going to be maintaining this particular table that in this batch all these tokens were there.

The Admin: If the in a batch came 47 times I will need to remember that this had come 47 times. Are we clear on this? Because I'm pulling it and I drag it there. That's the easy part. That's not what is going to be difficult. Now why this is important to remember is the consequence that matters lives in the backward pass. When we do back propagation, how do we back propagate? So let us say in a batch of 4096 tokens or let me draw again. So we have the sun rises in the east on the occasion of independence day the United States of America did something then we have on the other hand and so on and so on.

### 00:40:00

The Admin: So just focus only on the okay and this is the batch and this batch let's say had 256 as a batch and each pad had that 256 into 4096 tokens. So we have somewhere around a million tokens that are going in right million tokens from or million tokens the batch size and the inside this came let's say 67 times okay and then we have this embedding model that I told you where we have each row representing every single token now this came 67 time and this is the so question to you is in back propagation what do we do as I told

The Admin: There's a parameter back propagation comes and say dude you need to change right because you're not doing the right thing right now and the came 67 times. So back propagation has 67 edits what do we think we should do? We should edit it 67 times the half correct half wrong.

Abishek Ajai Satnur: some bridge.

The Admin: Anyone else?

Suresh Mantha: make the changes and send it to the tracker or the gather…

The Admin: No, no,…

Suresh Mantha: which you

The Admin: that's not the question. We've done all of that. We got the right ids or right modifications but in this batch I've done back propagation but now I'm about to update the weights in this batch came 67 times.

Sachin Bharadwaj: Excellent. you average and…

The Admin: So I have 67 edits for that. Similarly India came five I have five edits for that. What should I do? Edit the table 67 times for the edited table five times for India. That's a question.

Nikhil Shrimali: We accumulate for a certain batches and

Abishek Ajai Satnur: We'll sum it and…

Abishek Ajai Satnur: then divide it over the nor we'll normalize it after it.

Sachin Bharadwaj: multiple learning need. Take a small step.

The Admin: Is that the question I'm asking?

The Admin: Am I asking that should we change the value? I'm asking a very different question. Should I update the table 67 times or…

Suresh Mantha: Update this gather table once.

The Admin: should there be a one? We have to.

Abishek Ajai Satnur: Send it

The Admin: Yeah. Yes. So for the whole batch we going to accumulate the 67 times and whatever the update is there at one shot we are going to update it. That is why it matters because if you go with the online method that we multiply and do then you are thinking that you have to multiply 67 times. So updating a embedding table is actually very easy and that is why this widget is also there that will try and help you understand a bit.

The Admin: What is happening here is we have a batch that arrives it goes forward right batch is arriving we have a batch token 12 we can increase it also so let's say we had 40 tokens in the sentence example that we are sending but let's keep it small so we can track it let's say we had 13 tokens not a good number let's say we had 12 tokens only now zip fq is something which is interesting and will okay let me show you what a zip plan is. These are terms that keep coming in zen distribution sorry these are terms that keep coming in and there is no way I can create a dedicated session for this to explain it to you now unfortunately the language follows zip flan distribution or zip f distribution. What does it mean?

The Admin: It means that some of the words come very very often and some of the words come rarely. We think it's Yes. No. It's not common sense for all the fields but ziflan definitely there for the languages that we speak and for nearly all the languages follow something like this. What it means is that there are some words is going to be updated 67 times India which actually has a meaning is going to be updated only five times very less amount of time. So there's a big mismatch of how many times a particular words get updated and how many times one doesn't. But this and here we're saying if Q is one and we'll see what happens when I change it. So a batch have arrived. We do a In the forward what we realize is that these tokens read four time the token one token number three is read once four is read once and the once once once and so on. If I increase the total of tokens,

The Admin: then you're going to see that those numbers change basically right so batch tokens based on that some tokens again read less now we do back propagation when we do back propagate we are only going to be updating these rows this is the first thing that I've told you till now zip f is not involved yet let's look at again a batch comes in when we do forward we realize that this token came four and when you back propagate only those rows are back propagated so you can already see there are some tokens

The Admin: that will not be back propagated and the reason should be simple the whole batch was about India so why anything about Pakistan will be updated or that will be updated why about Chinese scriptures will get updated maybe it will not for a particular essay that we're talking about right so when we do forward we collect all the tokens that we have and we remember the number of times we had them when we back propagate we just sum it up and back and send it out all of you're saying average out do this do that not our task that is a task of optimizer when we discuss optimizer it will decide

### 00:45:00

The Admin: How to optimize and how to average out different sessions. So we'll not even touch that topic today. The problem is because we have zip fq this is what will happen. Some tokens are going to be updated a lot of times. In fact doesn't matter how many times you try going to see that some tokens are just going to be massively trained whereas some tokens which actually are storing meaning and have some response and are the answers for some of the questions will never get any propagation to go back and edit it. This is something that should immediately hit your head and say dude not only in Hindi or Indic languages we already have less data. Some of the important words in those languages will be even seen less. So they are going to be updated even less. This is like a starving engineer who could have made a jet engine but nothing has reached that particular person. Are we clear on The two concept we discussed. First is that we just collect and we back propagate at once.

The Admin: And here you'll see that not only the language domination is not in a favor of the indig languages or coding or any other topic that you decide not to add. Second, those languages also have tokens that are going to be updated massive number of times which are going to skew the distribution for the languages we are in favor of indic and other languages that you may want to actually work on right and that distribution happens is even more skewed because of the zip f features that a language have where a few words are used way more often compared to some other right for example in hana you'll have mcbc with a very high frequency whereas if you go to south not those words they will have a different word but each language will have its own zf

The Admin: that have kind of All right, questions. Suresh.

Suresh Mantha: Yeah. How similar is this token embedding ranking are different?

The Admin: What do you mean?

Suresh Mantha: Token embedding ranking also mean the most popular or used word takes the precedence over the next 100\.

The Admin: That is…

Suresh Mantha: And here we are not ordering But we are just capturing…

The Admin: why we want them to be already ordered so we have some idea. You're confusing two things.

Suresh Mantha: which of them are occurring more frequently.

The Admin: You're I'm number two in terms of money. Can we assume that you're richer than me?

Suresh Mantha: Yeah, we can.

The Admin: So the frequency the token ID It is not going to tell us how rich Are you rich by only one rupee or one trillion? You understand the difference? Zipf is telling you The frequency is just telling you that you are richer than me.

The Admin: So a word occurs more number of times will have a lesser ID.

Suresh Mantha: God.

The Admin: Fair enough. But what's the distribution?

Suresh Mantha: God. This is interesting things.

The Admin: Okay. Nan louder.

NITIN YADAV: Ron when we are saying that we are back propagating again so it is about changing the model weights or anything else which is getting changed can you please repeat again when we are mentioning back propagating today so…

The Admin: Today we're not even discussing model. I showed you how the transformer architecture is. We are at the periphery of the model. nobody shows you decoder only. And I hate that. The architecture that is used is not shown. Transformer moment you search you every time get this. This is the wrong architecture. This is the 2018 full transformer decoder only will look like this. Finally. So here we are seeing input embeddings. So we are just entering the model. So when we say back propagate everything will be updated.

The Admin: But today we're only focusing on this part. If okay you cannot update input embedding…

NITIN YADAV: what exactly we are updating if you have not Mhm.

The Admin: if this is not updated. So this will be updated. But today we are only focusing on the input embedding updates.

NITIN YADAV: Got it. Okay.

The Admin: We're not saying that we are only updating this. This has to be updated but we're not discussing it today. Okay. Bali.

Balaji Chunduri: So just to clarify the question you asked.

Balaji Chunduri: So is it going to update the frequent words multiple times or once just by default behavior…

The Admin: has to it by default it has to.

The Admin: So we are looking by default behavior.

Balaji Chunduri: but you're not coming to the actual behavior you have not explained.

The Admin: Hey, this is the actual by default behavior. Don't play with word.

Balaji Chunduri: Okay actual.

The Admin: This is the actual act honest…

Balaji Chunduri: So 100 times it updates…

The Admin: what happens default behavior.

Balaji Chunduri: if it comes 100 times.

The Admin: Yes. Yes.

Balaji Chunduri: 

Balaji Chunduri: Just one more question. So this is during LLM pre-training or is it like designing vocabulary stage? vocabulary so we take a design vocabulary and…

The Admin: We are in the training now. The design vocabulary is gone.

Balaji Chunduri: again during pre-training also we update the vocabulary again. So the vocabulary is not frozen during pre-training. Is that correct?

### 00:50:00

The Admin: How is it linked? The vocabulary tokenize everything is finished in session six. We're not touching it again because we fixed that. That is why we're on session seven.

The Admin: We cannot go back and…

The Admin: change anything. Moment we change that the tokenizer will change.

Balaji Chunduri: No, but no,…

Balaji Chunduri: I'm talking about updating the parameters during training. So vocabulary embeddings are also learning during this stage right when it comes to training they are like random values is it okay usually I mean my understanding is word toe or…

The Admin: Embeddings are learning now. We have not done any learning prior to this session. Correct.

Balaji Chunduri: glow come with pre-training but here it learns during the training itself right okay thank

The Admin: Here we learn all of those 8096 things are random. Abishek.

Abishek Ajai Satnur: Hi Rohan we spoke now about how different words in the data set have a different frequency right …

The Admin: Thanks. No,…

Abishek Ajai Satnur: how does this come into play when we try to decide which data goes into our annealing and pre-training because they have different learning rates so shouldn't we take words that occur less frequently into our kneeling Okay.

The Admin: the problem is words that occur less frequent doesn't discount the fact that it will always come with words that will occur a lot more number of times. For example, the and full stop, exclamation and so on. There is no way you can just send important words like India, constitution, diplomacy. It would just not make sense going towards it as we go.

Abishek Ajai Satnur: Is there a way to combat this problem of Okay.

The Admin: I'm just explaining the problem this and we have to think about it.

The Admin: Okay, we're done.

Vardhan Walavalkar: Yeah, I had a question about this embedding and back propagation. So that got resolved. I have one more question. So this embedding dimension in terms of terminology is as the model width. is it the same?

The Admin: No, no, no, no, no, no, no. has a contributing factor to it,…

Vardhan Walavalkar: And…

The Admin: but that's different. Correct.

Vardhan Walavalkar: and the sequence length is the number of u u tokens you present at a time to the model, so if you are presenting all the sequence I mean related to the position embedding. So if you are presenting it together to the model it is coming in a sequence anyway right?

Vardhan Walavalkar: So why do you need a position embedding in that case? Because okay Okay.

The Admin: Because all go at the same time model has no way to understand this is before this is later…

The Admin: unless we mention it. It's no when you have question that means otherwise also have same question right so let's go slightly deeper so four five and then here let's say these are the neurons that are coming in and these are the weights for example 0.1 and let's keep 0.1 only and then we have the result here so 4 into

The Admin: 1 is 0.4 and 5 into 0.5 is 0.5. Answer is 0.9. If I swap the location, it's again going to be same. That's a problem that new networks have, right? We Yeah,…

The Admin: it doesn't know the order because all are presented at once. We need to provide it some hint and that hint might be adding something here in second dimension for example right that's where if you remember what is this I not invisible bib remember imaginary so can we add information in the imaginary access the second dimension…

Vardhan Walavalkar: imaginary. Imagine it.

Vardhan Walavalkar: No. Okay.

The Admin: where at least I can store so now if this was 4 \+ 2 and this were 4 \+ 3 then from these location I can figure out what was the

Vardhan Walavalkar: Yeah. Thanks.

The Admin: M correct…

M: So Rohan you are mentioning that index tokens will get lesser updates. So just I didn't understand that but based on the frequency they will be getting lesser updates why does that happen?

The Admin: 

The Admin: because the word came less amount of update may happen less.

M: So at least the updates will be happening right.

NITIN YADAV: This zip distribution so is it a informative thing for us or using this can we change the structure of data which we are putting in a batch.

The Admin: no but we need to consider that that happens and figure out a policy or figure out something that can account for this thing and that is the section below so if I scroll we'll get some answers okay always remember and…

### 00:55:00

NITIN YADAV: Okay.

Dattatreya Manjunath: Yeah, so just asking if normalizing or scaling up the important words is a valid strategy for us.

The Admin: this goes to a very deeper fundamental and I've seen three algorithms that are proof of

The Admin: what I'm about to say if you think there's a solution to a problem and you implement that in a new network you'll see it actually becomes worse because when we think there's a solution to a problem we are only considering ourselves to n number of problems whereas there might be n square problems right maybe it's not required the ideal solution to nearly always such problem is to implement your solution but give a feature to a neural network to not implement that solution if it is not required It's a very different way of looking at how do we work with neural networks. The way we work with neural networks is we think there's a problem and we have a solution for that implemented solution but let new network decide to implement that in the real time or not.

The Admin: What you have done is there's a solution your network will look at the problem it will look at a solution I need that but when the problem doesn't exist your network is going to say the solution is not required right so behaves like a filter essentially so always think in terms of filter what can I do where I can come up with a solution give it to new network but let new network decide whether this is required or not the very beautiful way of looking at it. Batch normalization is example of it and you have loss function as a example of it and there's something called KL divergence that is perfect example of what I just said that solve it but let new network to not use it if it is not required. Yes sir.

Yasir Reshi: Yeah. So we have a frequency based update. More words, more updates,…

Yasir Reshi: less words, less updates. But what about the quantum of those updates? Is it scattered in a way that 0.1 where I have 57 updates and 01 or 0.1 where I have less updates to make the more impact?

The Admin: I'm so happy all of you are thinking in this direction…

The Admin: because it took a Nobel laureate to answer that particular question and think that deeper and his name is Okay.

Yasir Reshi: I hope you're not being sarcastic.

The Admin: No, no, no, not really. Jeff Dean, what is his name? I'm forgetting his name. The three guys, this guy, it took people like him to understand this kind of problem and then come up with a solution. These are the guys who wrote RMS prop, And you are exactly asking the right question which will help you understand why Adam is required or why prop is required. So, these are optimizers. What they do?

The Admin: They remember, dude, this guy is getting a lot, this is little like IT department. This guy is getting a lot of update. I need to do something. This guy is getting a less update. I need to do something about it. So, what will happen internally using these algorithms is if something gets updated a lot, the update sent to the model or sent to that parameter is going to be of lower quantum. If the update sent to the parameter it is automatically going to increase that update ua Right? It's like something like this 45 into versus 1 into 45\. So 45 updates of one were coming in and only one update of 0.45 was coming in. Let's say that was scenario. So when we use this kind of algorithm, it's going to say no dude this is the right structure and this is wrong probably something like this. So that is where Adam and others think come in. But it is not the session to discuss that. So I will not answer any question related to it.

Avnish Midha: Okay, maybe you may not answer this, but I was asking that instead of an optimizer, doesn't it even call for changing the data set to have more examples of certain things which are less updated?

The Admin: I knew you will ask the question.

The Admin: Yes, of course. But we need to remember the Zipline is going to cause some of the words to be really high. For example, the top and…

Avnish Midha: Yeah. Yeah.

The Admin: some words are going to be low. So, we can't throw away the zipline feature.

Avnish Midha: Yeah. Thank you.

The Admin: But we need to increase the data set in such a way that these words come often and unfortunately for example there's a particular term which comes less for example waterity let's say you want a model to understand water So we can't make a paragraph we use water city five times that's not the answer.

Avnish Midha: Yeah. Yeah. Yeah.

The Admin: So we need to be smarter about how do we package it language a lot of nature has a good distribution that is…

Pranabesh Dash: So the zipline is specific to words and languages. When you go to VLM or other kind of things like do they apply as well or it's just the language where this distribution language. Okay. Okay. Okay.

The Admin: why neural networks worked there the convolution network cannot here. Biology amongst other things languages.

### 01:00:00

Balaji Chunduri: So this zipline is natural behavior of language in general, any language.

The Admin: Yes. Yeah.

Balaji Chunduri: I mean so it depends on even humans have to learn based on this nature of zip lang. So do these people in get some inspiration from…

Balaji Chunduri: how people learn and adopt these techniques?

The Admin: Everything is based on…

The Admin: how humans learn.

The Admin: In fact, only the neurological cross-section between computer science and neurology help people come up with these architectures not most some but inspiration does come from there because we cannot make a spiking neural networks on hardware today. So it has a limitation of how much it can affect. So now let's talk about the table cost and closing the in session two we said that the vocabulary size that we have 131k 131,000 tokens and it is already larger than many complete models right because the So what you need to realize is that a parameter count is really easy to count. We have v into d.

Balaji Chunduri: So most of the techniques to compensate are based on human behavior. Okay.

The Admin: In our case, we have 131072 multiply by 8096\. That gives us around 1 6 billion parameters that we need to train. there's a concept of tying. What is this time? And what do we need to know? This is our neural network and this is our In input layer we have 1 3 1 072 tokens and each token has 8 0 96 embeddings. let us say the is going in. So what do we do? We go to that huge table. Go to the figure out that particular thing and place it here. Right. So this is the input embedding essentially. Let me write 1 3 1 072 and 8096\. This is the input.

The Admin: The output happens to be reverse. Output is going to be 8 096 and 1 3 1 072 on top. So depending on what 8096 number went in, it is going to say I am the right. Let's look at it again. In the model, Any word of 131072\. Clear on this? What can we send to What can come out Any of the 131072, It can only tell you the token. it can read, right? So, the output is also one of the 131072\.

The Admin: So if you look carefully the input dimension is going to be 131072 cross 896 and the output side is going to be 8096 what the model predicts that goes inside a 131072 matrix and one of them says I am the one right so these are exactly inverse of each other at least mathematically are we clear on I'm talking about…

Umesh Nmenon: Hey Rohan, this you are talking about the word next token prediction,…

The Admin: what correct word one comes in.

Umesh Nmenon: So any word that can go in and you are predicting. Okay.

The Admin: Word two comes out.

The Admin: Nothing. Good question.

NITIN YADAV: So Ron just a simple question if we have 131072 \+ 8096\. So how will we know that is the word are we taking average and the maximum out of 131072 tokens is considered that okay yeah this one is the token.

The Admin: So we have 8096 numbers predicted by the LM. Say yes.

NITIN YADAV: Yes. Yep.

The Admin: This goes inside a neuronet network. The neuronet network happens to be 8096 cross 1310 72\. Right? this is going inside a matrix which is 131072 cross 896\. Clear? what will happen? we have How many slots? I'm not going to draw all but these many slots and they will have some numbers predicted inside. 0.67 0.93 here number might be 0.10

The Admin: 1 Z blah blah blah and so on.

NITIN YADAV: 

NITIN YADAV: Thank All right.

The Admin: So we took the max and say this is what the model is predicting. How do we know this has to be predicted? Because we said to the model that you have to predict this one hot vector right that's a prediction itself that's not back propate loss also that I wanted one you gave me only 0.1 take a punishment of 0.9 that's back propagation also. So not only we want that thing to be max we also want that thing to be one…

The Admin: because 0.01 and if this number was 0.09 09 they're too close for my comfort. So that we'll discuss later on. But this is how we understand what the model is trying to say.

### 01:05:00

NITIN YADAV: so in the prediction I agree it predicts the probability…

NITIN YADAV: but in the initial phase when you are saying that it's 1 13107 2 \+ 8 096 so it's basically a representation right so of our complete table like the tokens cross embeddings so there…

The Admin: Okay.

NITIN YADAV: 

NITIN YADAV: 

NITIN YADAV: how we know D is going.

NITIN YADAV: So there we should take the average right out of the embeddings. Sorry. Yes.

The Admin: we know the going in.

The Admin: How do we know the is going in?

NITIN YADAV: How would I know that the is going in?

The Admin: That is what we discussed in the first section itself that I have a table of 1376 and 8096\. I know the is wanted. So I pick that dimension and then give that to record.

NITIN YADAV: Okay.

The Admin: So that's in manually being done.

NITIN YADAV: Got it. Thank you.

The Admin: So what I want you to take out from here is that we have this 131072 into 8096 as the input embedding and output side happens to be 8096 of 131072\. So there's something the concept is called weight time. Why don't I use the reverse of it? What do I mean? So my input side is 131072 cross 8096\.

The Admin: output happens to be also 1 13 1 072 cross 8 096 this is reverse by the way but logic is why don't I use same right so this is called weight time for small models it makes sense because I'm doing exactly what the matrix wants and it acts like a small regularizer also regularizer basically means some additional information for it to perform better so again what is happening parameter comment is easy to understand we have 1.6 6 billion parameters just in the embedding layer and if you untie them we have 2.12 billion. Untie basically means the top layer and First layer and last layer can be same. We'll talk about when If they're not same then we are talking about Two billion parameters because the model width we have in this discussion kept to 8096\.

The Admin: The final models is predicting age of 96 numbers that goes inside a matrix that is 13 1 072 cross 896 and of them only one is the token that is being predicted right are we clear on this the number actually has a bit of memory associated with it a parameter being trained under AdamW and I want you to remember this always because in future also we'll have the discussion a parame being trained under ADMW. AdamW is one of the many optimizers we have. have we have Adagrad, we have RMS prop, list goes on. AdamW is the most famous one that is being used right now. We in V5 have not decided to use ADMW yet because there's a new optimizer that the Chinese are using and they're showing a lot of great things about him.

Abishek Ajai Satnur: Move on.

The Admin: It's called Lion or something like that. we might be exploring that optimizer also. But let's say we are talking about AMW.

The Admin: In ADMW, every single parameter has to have 16 bytes per parameter. Which means that if our emitting layer is 1061 or 1 billion parameter that we spoke about we are looking at 17 GB of RAM just for the emitting layer for one batch. I imagine that number of batches we have and how much memory it will take right so it's not just about the model weights because let us say we're talking about training 120 billion parameter model and of that we're talking about one billion parameter for our embedding layer so it's not much right 120 is to1 ratio but in the RAM is going to be a lot because we have to store all of that okay let's look at here same thing now it's explained in terms of the parameters and the overall

The Admin: All things that we have model width 8096 the input was 8096 somebody asked that does the embedding dimension is equal to the model dimension answer was no here assuming it is yes because that allows me to calculate things easier but answer is not linked you can decide it to be same so if the model width increases you're going to see that overall parameters change if the model width is 512 which means every layer is only 512 embeddings

The Admin: Do you even get what I'm saying or just nodding your head? something that we have to decide. we decided that we have 131072 cross 8096\. Do you remember this discussion? I was talking to someone.

Abishek Ajai Satnur: All right.

The Admin: I was explaining the bandwidth.

Suresh Mantha: Dimensions.

The Admin: You remember this Inside the model also we have to decide what is this number going to be? Is it 4K? Is it 8K?

The Admin: Is it 16k? That is the inherent capacity of the model to calculate on. So this is the internal bandwidth of the model. Right? That is what we're talking about. And this determines the size of the model very very fast. This can be a low number like 5112\. If you're talking about SLM, you are never going to be training more than that. That is what defines an SLM. Not that the model parameter is 2 billion. This is what SLM is going to be. Fast, small, and good enough for doing simple things. If this goes to something like 18K, you're talking charg level, So that's the main deciding factors and that is what you're seeing here. You can see that how fast the model weight stop input emitting total transform stack. Look at this number and I'm changing it right here. We have 12,000 as the width and you can see that immediately we have reached 100 billion just here. Okay, let's keep it to some number.

### 01:10:00

The Admin: Let's say we keep it to 8 096\. look at the vocabulary. If the vocabulary is small, transformer stack is not changing that is 37.75. What is changing? The input embedding and the Correct? That will change because if my vocabulary is bigger, then I have to use more just convert my parameters or my tokens into something I can feed to a neural network. Right? So this is deciding how many parameters I have in the overall model. So let me keep it back to somewhere here. the number of layers, how deep are we going? as we increase this, you're going to see again the transform stack is changing.

The Admin: Right now we have This is again something interesting. We have not touched it. Then we stretch it and then We stretch it and we compress Something like that. So this is that To be able to process thing we need to expand. Then we need to work on it. Then we need to compress and then we need to go. So this is the FFN multiplier. So if you have 8096 at the bandwidth at some stage we are making it 32,000 and doing some magical work and then we're compressing it back to 8,000. So this keeps happening right and when we're discussing the architecture that is also massively expensive and this is again determining how much bandwidth we have. If this was tired then the head and the tail are same and that will directly work for us. Now this is 80 GB accelerator which means we have 80 GB of RAM on our GPU.

The Admin: If you had more RAM then everything can push it here for 4x I'll go 8x 131 we can go to 252 then we have some problem but here still works right but if you are working on a poor GPU it's going to do can't happen okay so whatever is there on the screen do you have any questions related to this anyone say Model width is not the embedding dimension.

Syed Abdul: Model width is the embedding dimensions, right? Yeah.

The Admin: Model width you can decide to be equal to embedding dimension.

Syed Abdul: I mean the dimension of each of the vector across.

The Admin: You said yeah I meant some they're not same.

Syed Abdul: 

Syed Abdul: Yeah. Sorry. I mean but

The Admin: Are we Can be same balaji.

Balaji Chunduri: So just to clarify my understanding so you mentioned this 170 131K is the vocabulary size and…

Balaji Chunduri: 8K is the dimension that is going in.

The Admin: of the work or…

The Admin: of the model. Both are different can be same Correct.

Balaji Chunduri: Yeah. Yeah. Yeah. Yeah. I understand. So now that is going into the model as maybe sentence length and then comes out again models dimension if it is 8K. So that is what you are seeing at the output is 131k into 8k and then on top of this there will be classification head one half okay…

The Admin: Classification we are doing detection directly. The one hot vector is coming out. 131072 is the output. Yeah.

Balaji Chunduri: but why do you say 8k into 131k as a dimension in the output it's just the model's output on top of it the classification or happens You're saying before the Okay,…

The Admin: The classification input vector is 8096 in your language.

Balaji Chunduri: that is before the classification, I mean that's what you meant by the dimension.

The Admin: Correct. Okay.

Balaji Chunduri: Yeah. Got it.

The Admin: Nothing. okay.

NITIN YADAV: So run the input heading and the output heads they are equal. So is it a necessity or a good to have thing?

The Admin: So the mathematics of it is simpler and preferred. That's…

NITIN YADAV: Okay.

The Admin: why they're nearly always same and…

NITIN YADAV: Got it.

The Admin: I've not seen an instance where not same basically if I were to say that and one instance it was not same was V4 model and…

The Admin: you'll see immediately why it was not same in the next session but in 99% cases they

NITIN YADAV: And one more question like when we go from the embedding layer to the model width…

### 01:15:00

NITIN YADAV: which you are saying that right now we are keeping it same just for a thing but whenever we have a greater than or…

The Admin: Yes. FFN multiply is completely different.

NITIN YADAV: less than thing. So this FFN multiplier is there some other mechanism working on there? Yeah. Okay.

The Admin: FFN multiply has nothing to discuss with what we are doing. see this model you see feed forward that is that feed forward thing so it happens inside each transform block so not related to whatever we have and we have to decide it's 4x or 2x justification

NITIN YADAV: So the layer which we have from the input embedding to the model weights. So is there some engineering mechanism there also how would we convert the vectors to compress or make it to other dimension.

The Admin: ation but we'll discuss that.

NITIN YADAV: Okay. Thank you.

The Admin: Abishek Ajinat.

Abishek Ajai Satnur: Rohan when the diagram is saying tokenf facing matrices against one accelerator is there any other overhead that we have to account for even after this or…

The Admin: Yeah. …

Abishek Ajai Satnur: is this the full usage of the VRAM at this point with these dimensions and band meters.

The Admin: we have the bat size. Every single token that is coming in.

Abishek Ajai Satnur: So right now when it says 42% that means the batch can only be at a max of two batches because then it'll be 80% per GPU.

The Admin: That's correct.

Abishek Ajai Satnur: Okay.

The Admin: That No, this is not what saying the two mates that face the vocabulary are consuming 42% of one X before a single attention has been placed. Which means of the ATGB 33.96 is just the input layer.

The Admin: we have not even went inside the model.

Abishek Ajai Satnur: Okay. Okay.

The Admin: So this is definitely not going to happen for process properly.

Abishek Ajai Satnur: Okay.

The Admin: It has to be something like 25%. Okay, I can at least process few words.

Abishek Ajai Satnur: Got it.

The Admin: Okay, can you lower your hand if the question is done? I'm not sure.

Adinath Auti: So the input embedding and the output head are tied are the weight updates also common for both?

The Admin: So it helps double weight update in a single run. So helps a lot.

Adinath Auti: 

Adinath Auti: All right understood. And is there any case where model width can be greater than embedding dimension?

The Admin: Never maybe smaller…

Adinath Auti: Okay.

The Admin: but never bigger.

Adinath Auti: Thank you.

The Admin: So There is no embedding with different dimensions.

Soma Korada: Rohan, I'm getting confused with the input embedding and output head. If both are of the same dimensions and if you're saying output head is one hot encoding is what is expected then where is the embedding getting trained with different dimensions?

The Admin: All embeddings have exactly same dimension.

Soma Korada: No, no. As in different positions in that 8096 have to be like the bank example there are different properties right these 8096 are different properties of explaining the word bank correct so…

Soma Korada: where if we are saying one hot encoding and then it's only one position of that whole 8096 vector which is taking bank Okay.

The Admin: that one position is 8096 numbers.

The Admin: So when you say we updating one token, you're saying you're updating 8096 positions or 8096 dimensions of that token.

The Admin: There's no one number updating 8096 values of bank.

Soma Korada: But you mentioned that we are trying to say…

Soma Korada: if bank's position is fifth position in that 8096 we're trying to just make the fifth position.

The Admin: Completely wrong.

The Admin: One second. What I just said is completely wrong. Bank position is fifth in the sentence. It still has 8096 dimensions. Where are you lost?

Soma Korada: Yeah. Yeah. It still has 8096 but that one hot encoder which you mentioned in that fifth position of 8096 has to be one bit.

The Admin: Who said that?

Soma Korada: Is that what you're saying?

The Admin: You're completely lost.

Soma Korada: Yeah. Where is this one hot encoding coming into picture is something I'm not Yeah. 8096\.

The Admin: Are we clear? Okay. What has to be the output size of the model?

The Admin: completely wrong. You're lost there only. Anyone else who thinks the output size of the model is 8096\. What is the output size of the model?

Abishek Ajai Satnur: God literally says,

The Admin: 131072\. So, are we clear on this? The output has to be 131072\.

### 01:20:00

The Admin: If your vocabulary is 5,000, the output has to be 5,000. if your vocabulary is 16,000, the output has to be 16,000 because does it say this word? Remember classification are Yeah.

Soma Korada: So here we are saying one hot encoding then Got it.

The Admin: So this means those 8096 vectors.

Soma Korada: And Okay. Got it.

The Admin: S not that thing is never low rank even after deployment or…

Sachin Bharadwaj: Hey Rohan, so for training embedding metrics, do we train a product of low ranks.

The Admin: on that is the most important layer and that is one big issue that is there that we can't low rank those things.

Sachin Bharadwaj: And the other thing is intuitively Rohan is this weight tying I think so…

Sachin Bharadwaj: if I refresh you see the 8096 vector that goes as an input to the model and what comes out is actually totally transformed right because it goes slow yeah…

The Admin: What comes out?

The Admin: What comes out from the model is also a 96 vector which has to become 1013 1 072\.

Sachin Bharadwaj: but did I get it but the information in the transformed contextual vector that comes out from the model and the one that goes in right It's different. So I mean the weight time doesn't make sense intuitively to me. I mean is it understanding correct?

The Admin: No, not correct.

Sachin Bharadwaj: Because I mean okay then what's the reason that you can't do weight ting on a models?

The Admin: Have I mentioned that you're at the end of the session?

Sachin Bharadwaj: No. okay.

The Admin: So you have to ask question related to what I've said till now. Raj allergy.

The Admin: Raj. Same model.

Raj H: Is the same thing used in every other applications also like say law or…

Raj H: research would we be making the same kind of models same approach

The Admin: No difference. Yes. Okay.

Balaji Chunduri: So yeah, so here I'm just trying to understand the input size which is one you mentioned it as 16 GB and output is also 16 GB here 1 GB yeah RAM memory there was a mention of input side let's say 131K into 8K that takes some memory right and…

The Admin: Where did I say 16 GB?

The Admin: That's a RAM. Correct.

Balaji Chunduri: then output side also it is the same memory you're talking about so just to clarify this So let's say the input vector dimension is 131 into 8K and then let's say the sentence length is 10 long sentence and…

The Admin: Correct.

Balaji Chunduri: then we pick 10 8k values and then these 10 8k values goes to the output and they are again 10 8k values right at the output of the llm. let's say we need to have 131k as one hot representation. When it is one hot representation, it is going to be 131 \+ 1, right? It's not 131 \+ 8k. So at the output, why do you say 131 cross 8k?

Balaji Chunduri: It is just one heart of 131 \+ 1 I'm confused on this point.

The Admin: This is the output head size.

The Admin: You're talking about the neurons that got created. I'm talking the weights that are creating neurons. So, okay.

Balaji Chunduri: 50\.

The Admin: So, specifically to you, You don't ask what you understand and then because you're short in time also, Answer this question. 7 into 8 is what? 56\. Seven things go inside. How many come out?

Balaji Chunduri: Sorry, I didn't get this, but eight comes out.

The Admin: 7 \+ 8 is a matrix. How many weights are there? You said you are comparing 8 with 56\.

Balaji Chunduri: Okay.

The Admin: You're talking about this. Clear. Okay.

Balaji Chunduri: Yes. Yes.

The Admin: said they are nearly always same.

Syed Abdul: So model tying can only be done when the emitting dimension and model width is same And the second question is when we say model time do we use the so in back prop you will have two times the weight update for its output…

The Admin: We update two times.

Syed Abdul: but so empirically will it learn better or will it learn more faster or is it okay?

The Admin: There is a caps to that that is below the section.

Syed Abdul: Okay, sure. Thank you.

The Admin: Okay, next.

Max: in one of the previous sessions you mentioned that weight ting is for small models or maybe large model maybe I'm missing it kick.

The Admin: Wait for five minutes, please.

### 01:25:00

Deepjyoti Saha: So the output layer is 131k that is the cap size right. So let's say…

The Admin: All right.

Deepjyoti Saha: if the model predicts token ID 20 it is actually going to predict the embedding so how is the last layer 131k? Shouldn't it be 131k into the embedding dimension? So, that's The second question is if it has Yeah.

The Admin: Stay there. Others also have the same issue. So let me first answer that properly. So our input layer is 1 3 1 072 cross 8 09 8 096\. What does it even mean? It means I have 131072 rows. Say yes. Okay. And then I have each row containing 8096 numbers. Say yes.

Deepjyoti Saha: Yeah, that's good.

The Admin: This is TH going in.

The Admin: And the t happens to be 10 01 token ID. So the text that came in was 10 01\. The got converted into 101\. That's a task tokenizer. Say yes.

Deepjyoti Saha: Yeah. Yeah.

The Admin: 10 01 goes inside the embedding table. Now this number goes inside my neural network.

The Admin: Does something and stops here. Output here happens to be a 96 say yes.

Deepjyoti Saha: Okay.

Deepjyoti Saha: Okay.

The Admin: After this we need to have something called an output head which is going to take this 8096 and convert it into 131072 numbers and…

Deepjyoti Saha: So that is the output head.

The Admin: of them this is predicted.

The Admin: So the came out. America. Exactly.

Deepjyoti Saha: The output head does a translation from a single embedding to a one hot vector which corresponds to your vocabulary.

The Admin: What does this embedding look like?

Deepjyoti Saha: Okay. No,…

The Admin: This looks like states.

Deepjyoti Saha: this is clear. Thank you.

The Admin: Okay. No.

Soma Korada: Sorry. can I just ask one question?

Siva Ajjapu: Hi. Yeah. Can you please go to the presentation and show me that can you please in put the bar layers bar to the more bar 48 and what are the transform parameters?

Siva Ajjapu: What is the math behind it? If we have vocabulary size 131k and…

The Admin: Math I'm not going to explain.

The Admin: Math will be explained in next few sessions. You just need to remember that this is…

The Admin: how it is changing. When we are changing this, each layer will have multiple sections. We have attention, we have input layer, we have KQVE. We have not discussed any of that. So can't explain that math today because we have not even talking about that. Second question. Okay.

Siva Ajjapu: Okay.

The Admin: All right.

Umesh Nmenon: So Rohan, other than the money, what is the science behind choosing PF164 weights and let's say FP324 other things? what is other than money? What is the science behind choosing FP16 or BF16, FP32? Okay,…

The Admin: When we talk about that, I'll share a paper and that paper is something that we use in V4.

Umesh Nmenon: Defense.

The Admin: There are some science s before goes to 8096 cross 1 31072 matrix and…

Soma Korada: No, no so from the 8096 which is predicted, if you go back to that screen, how does the model pick the token ID based on this 8096 vector? Because the maximum of it.

The Admin: output is whatever and the soft max. Yes. Well done.

Soma Korada: Okay, good.

Vardhan Walavalkar: so when you say the model width so that is because you can parameterize a transformer model with a parameter like a model width so all the internal say matrices and all are having a similar kind of dimension right that's the reason and…

The Admin: That's correct.

Vardhan Walavalkar: when you say ffn it's the feed forward network part of it that you are saying that we can expand or reduce okay thanks

The Admin: That is Okay. So with layer

The Admin: Unfortunately we have to wait for next sessions for that. the tokenizer and the embedding are one design surfaces. So when you decide a tokenizer you have to decide on the embedding and you have to understand the effects of both of them. The dial pulls both direction at once. A similar vocabulary definitely means lesser rows lesser number of parameter but it raises Fertility we discussed earlier also we want the fertility to be one for every single language which means that total number of token generated for a language needs to be equal but that's not true. 1.2 is a really really great number if you can hit that. So if you have a vocabulary which is small I will have to use more of my tokens to represent the same language right that will increase the fertility.

### 01:30:00

The Admin: So that will mean that manuscript is not one word manu and script it will be represented as two tokens right that means that I'm going to process more but if I increase my vocabulary manuscript might come as single token and if it does that then I have to process less which means that if I reduce the vocabulary my model size can be smaller the amount of RAM required can be smaller but I pay in the cost of more number of tokens If my vocabulary is higher, I do not pay in the processing because now I have to process less number of tokens but now I pay in the model size. So it's tied at the same time. So tokenizer and embedding are like they have to balance out each other. So there has to be some science behind what do we do and this widget is trying to help exactly on that. Now here we have some mixtures.

The Admin: We have E5 mix, we have English only, we have indic heavy and we have code heavy. And that determine the percentages we have for each of the tokens that are there. Then we're talking How many vocabulary we have? We have 1 131072 and other numbers. You can play around with this. Then we have the model width which it can be 12K and other numbers. Let's keep it to 8K. Then we have fertil sensitivity. This is interesting concept. If you go deeper then you'll understand further. So the only thing I will touch upon here is if the fertility sensitivity comes out to be 0.22 22 you can put it back into the math and see What it means is if the sensitivity is 22 then if you double the vocabulary it improves 14% fertility only which means that if I double my vocabulary of Hindi tokens in the tokenizer from 1,000 tokens to 2,000 tokens my fertility will only improve by 14%.

The Admin: Increasing vocabulary double to a double number doesn't mean that my fertility will drop tremendously. Remember Zlan if you're increasing your vocabulary does mean that you are adding more words but the zipline is very long which means that the word that you added the contribution is still not going to be 100%. Right? So there's a mix of that and it depends on how good your section is but this 22 is something that is sort of already at a sort rate. So what is going to happen is as you increase the vocabulary. So there are three things you need to look at.

The Admin: We have a token bill which is the attention compute which is shown in the blue. Then we have the parameter bill which is the embedding layer which is this purple. And then we have combined index. How much money are we spending right? We are how much combined memory is used or computation is used. And we need to balance this out. As I said a bigger tokenizer or a bigger vocabulary is better because I have to compute less but now I use more RAM of it which means that I need to go for a bigger GPU which has bigger RAM. If I use smaller vocabulary, I can sustain myself in a lower RAM but I need more processors now and that will again require more computation. So there needs to be a balance where we can fit both of them. So the situation changes for different scenarios and we need to find where exactly we are. This is where we are four was there right?

The Admin: this is so based on different for example English only we are 53.5 is okay but you go for a V5 mix then we need to be at least at something like 101K that is where the balance sort of comes in right and these are look at the fertility share we have 1.24 we have 1.43 43 Hindi 2.1. So if we can improve the fertility, these are the fertility we had earlier, then we can actually reduce the cost compared to English also. So it's not that you just decide that my vocabulary is 131, my embedding is 8096\. We have to come back with this kind of analysis of how much are we paying in compute, how much are we paying in memory and both needs to balance this. There needs to be a justification proper which says that that sounds like a real accurate thing. Can we answer this today? We don't have data set.

The Admin: only after we have data set, we have a tokenizer, we can merge both the numbers, do a short compute and then figure out that's the right structure that we have and we have to live with it. It's not that you have 131072 and the math says that you can go with 1013 and you decide to go out with that. not possible because this number has to be a really good multiplier of two power. If it is not then GPU is like a truck can hold let's say 4,000 toothbrushes. Can you send one toothbrush in a truck? Answer is yes. But the whole The GPU is like that. You can decide that I want to spend only this much. But That is about GPUs. It assigns a big memory block. The best way is to fill it up. So even if the number comes to 101 something, we still have to go to 131 to make sure that GPU is actually performing better. Sometimes it performs worse if you don't use it fully. Those things are going to come and haunt us back.

The Admin: The cheapest thing to do is to basically weight tie the bottom layer and the first layer. We tie both of them and if we do that we save some RAM and we get some benefit of regularization also. But what people have seen is the weight time is something that people are doing at a smaller model. It stops paying as the model grows, right? Because the percentage link to the drop in weight is not big when the model itself is big. So GPT2 tied it, gamma ties it, llama 2 at 7 billion does not tie it. So it goes something like this. Our vocabulary is 13172 and we are training a weight class. You see 5% below. So if we are somewhere over here around 30 billion people stop actually using it. This is something that you'll find in most of the model that are there.

### 01:35:00

The Admin: So the performance benefit or the RAM benefit of weight tying is not there if the model model is more than something like 3 billion itself. So if the model is small if you're training a SLM weight tie if you're not training SLM do not tie the benefit is not there and it goes back to the same question if the bandwidth is small there's not much to learn there you can tie it right because anyways the context is not going beyond but if you want a model to be deeper to have a deeper meaning and understand then the output and input needs to be slightly different right and we have done some studies also where a big model is trained and we compare the output with the input

The Admin: And you will see there slight differences and again those differences are something that makes a model behave like opus or something like Gemini and that is very important. So wherever you see the weight time anyone says weight time it's a two billion or smaller model. So all weight SLMs you are going to have both of them Any question on weight time No, you don't have any weight time question. Sachin math is correct.

Sachin Bharadwaj: So I think Rohan mathematically I mean weight ting is correct thing right? I mean respect to the model size empirically you're saying it's so just…

The Admin: Empirical. Yes. Correct.

Sachin Bharadwaj: because based on empirical evidences we are saying if you don't have SLMs then don't target right. Okay. Thanks.

The Admin: Okay, I will check.

Abishek Ajai Satnur: But Rohan, I think session 3's homework asked us to make a 40 billion parameter model that outdid Gemma 4, which was 30 billion in size. I think the weights were tight in that model architecture. How come they tied the W? Do you have any insight on that? Okay.

The Admin: I don't think so. Weights are Small models 3 to bigger models. Gamma is a small 4 billion model. factoriize embeddings on the ramp. this is where so you can read it out, but I'm going to explain you what this actually means because this is easier to explain using drawing compared to just reading it out.

The Admin: By the way, the concept we're about to learn is going to be used in LoRa and a lot of different places. So, be sure you understand what I'm talking about. Okay, let us say we have a 8 0 96 vector. Okay, now this is called rank specific to what we are discussing.

The Admin: It means a lot of other things also but this is very specific to what we are discussing ranks and there's a word that I like to use and that word is there in the yes

The Admin: So, let's say we have 80\. more important than that, have you heard of what is the best streaming platform? Anyone who's into audio?

Yasir Reshi: Spotify.

Vardhan Walavalkar: 45\.

The Admin: You're not into audio then if you're saying Spotify.

The Admin: Anyone else? There's something that seems at very high. Apple is trying to compete with them. Why is title famous? High bit rate. What does it mean?

### 01:40:00

Vaibhav Lohar: title they give it at five high bit rate so basically…

Abishek Ajai Satnur: Better quality.

Vaibhav Lohar: how much data they are sending per bit Please see this number.

The Admin: How much you're sending less? But what does it mean? they're sending better quality, And if you're not into music, then if you hear title, Spotify, YouTube, you may not find any difference.

The Admin: If you're deeply into music, you're going to say how are you even comparing? It's like comparing iti with IT T, So that is how angry some people will get. that is exactly what the spectrum is. When we have 8096 dimensions of a particular word, is every dimension important or we can actually reduce it? Right? Of course we reduce it, we are going to have a lossy compression. We are reducing the overall bandwidth it can carry. But there are some dimension that you can throw away. And while learning we also realize that it is possible to compress it to some extent where the loss is not much. Same happens with JPEG as well. So if you look at JPEG compression we will have different ratios right? So a file size of 248 looks like

The Admin: This a 22kh looks like this is again a very very weak compression 1 is to 10 45 is to one here's a compression factor 50 25 18 here is again compression and compression right now here if you see I don't think you can find a lot of difference there so there's some compression you can already do and that compression is important because we have big models and we can actually draw that down dotted down basically means that we can live with a smaller model by faking that we have a bigger model and this is something we are going to see a lot. So we said that we have 8096 as the model dimension So this is let's say going in the layer 1 we do something here and it comes out as 8096\. Are we clear on this? Something is going to happen inside. What we can do is if you can figure out the rank properly like how much is good enough.

The Admin: So we can actually do a matrix multiplication of this with 8096 cross let us say 512\. So we take 8096 compress it down to 512 compute everything is 512 and then do the reverse of it. We take 512 which is about to come over here convert that into 8096 and give that signal out. This thing is the ranking that we're talking about. How small can we go? This is something we have to find out. What we will also learn is once the neural network is actually fully trained, this number is a very Final dimensions which matter for every single operation inside network is actually very small. All the other dimensions have been thrown out because they're not relevant because they were carrying signals that I don't need. Each token will need a different kind of signal and each layer focuses on processing some bits of it. 8096 is coming in.

The Admin: If every layer or every neural network inside a transform block starts working on every single 8096 number, then they are overcompeting or they're not doing the specific job. My job was to find out whether it's a noun. Your job was to figure out it's a verb. And I do not have to look at All the verb kind of features are in specific dimensions. All the nouns are in specific dimensions. So we can decide that is what happens inside a new network. Especially when we are in the late training. These are the things that lead to the concept called Lora and other things. Lora is literally that low rank adaptation. So we take a model figure out what are the small dimensions I can work with and only train those dimensions right so these feature are going to come in but this concept is about the same thing the factoriization that we can take a bigger matrix we can make it smaller and mathematically it's exactly same and the reason is exactly same is because 100 cross 100 can be written down as a 100 \+ 10 and 10 \+ 100 right the output behaves exactly as the same thing Abishek

Abishek Ajai Satnur: Hi Rohan. I just wanted to clear up the meaning of rank. So I've come across rank rank.

The Admin: Rag. please wait.

Abishek Ajai Satnur: No r k.

The Admin: Okay.

Abishek Ajai Satnur: So sometimes there are rank 48 layers. Is that the same thing we're talking about right now. Is that different?

Abishek Ajai Satnur: 

The Admin: Rank zero.

Abishek Ajai Satnur: Yes. Yes.

The Admin: Rank zero. If you're counting from zero, then you rank zero. Can you wait till the end of the session or out of Google?

Rubel Chowdhury: Is it the same as rank of a matrix? Okay.

The Admin: The smallest dimension or two dimension basically, right? you are talking about different rank and here I'm talking about different rank.

The Admin: Look at what is happening here. We have a vocabulary of 131072\. We have a model width of 8096\. The bottleneck rank here. If I change it, you're going to see that if it changes, we are deciding of 8096 how many are we going to carry, What is the rank I'm going to into? I'm going to convert that 6 into 8 I'm going to convert that into 2708 or a bigger number, right? We don't know that. then there's a spectrum decay. How fast is it decaying? the spectrum decay will be very high if the model is trained. The spectrum decay is going to be very low the model is in the initial part of the training. So that's where the confusion comes in. If this was not true then you can do this low rank adaption for all the layers and actually train that only. But this changes as we train the model. So from one literally it will go to some much bigger number as we keep on training.

### 01:45:00

The Admin: This means if the model is trained I can actually reduce this a lot. I can go to something like 800 to 110th and save 100 times computation to get the same result. But this happens as we train the model. Are we clear on it? Okay. session.

Sachin Bharadwaj: Yeah, can you please explain spectrum? I didn't get it how it is defined.

The Admin: How fast the signal is dropping? How many dimensions are required to represent it as of now?

Sachin Bharadwaj: But how do you compute that? I mean Yep.

The Admin: So you see very easy to compute. You tell me how do we calcate that? We have a 10 numbers come out. Okay.

Sachin Bharadwaj: Yeah. Yeah.

The Admin: I do 10 \+ 2 and then do 2 \+ Yes. 10 number go in,…

Sachin Bharadwaj: Yes. Yeah.

The Admin: 10 number come out. Compare these. Very easy. How close are we? two? three? Are close at four? Are we close at five and six and very easy to calculate.

Sachin Bharadwaj: Basically do a sweep. Okay.

The Admin: Yeah, this is…

The Admin: what is going to tell us the difference. compression factor can reduce a model with further…

Deepjyoti Saha: So model width is the compression factor right is that correct?

Deepjyoti Saha: Model width is the compression factor. Okay.

The Admin: but model with remains that 10 or 8096 inside we can reduce something but the whole thing is 8096 we don't touch that Because

The Admin: A lot of places used.

Deepjyoti Saha: Okay.

The Admin: Okay. Deep do.

Suresh Mantha: What's the most preferred model that compression factor that means that…

The Admin: What do you mean by that?

Suresh Mantha: what we compression that okay for before again that changes every time we run into a different type of interesting

The Admin: Most preferred We have to determine for each same formula I said 10 10 compare that and we figure out at that stage this works. Yes. comes the paper that I wrote last time. This is the chroner. let me show it to you. This is me showing chronoker embedding. this is what we wrote last time. It was published as well. chronograph factoriization. this is the logic and this is how the thought process went.

The Admin: And I want to explain this because assignment is You are supposed to write the chronoer embedding 2\. So let me see can you come up with some interesting concepts or not. So I was thinking I have this 1372 ken Fair enough. And all I have to give the model is 8096\. Are you with me till this point? The model doesn't know I have 1310 72 or I have 52 or I have something. Model just need that 8096\. And I have to store this big ass 131072 cross 8096 a gigabyte of table and in that table I'm going to pick a row and send that clear on So this is the starting point. So I thought why can't we have a method in which I can create that 8096 without having that table.

The Admin: Can there be a method in which I do not keep this 1 131072 cross 8096 table but still can create that 8096 number for each token and that is what chronog factorization is right so in chronoker embeddings do not keep a row at all we build it at the real time and the whole thing is there and you can read it but I'll explain how I did it and that will be much easier if I just solve it. What I did is and this is finally how I ended up u deciding the final algorithm I'm explaining and the final shape of it. The limitation of what I did arrived at that I can only have 32 characters in The character maximum word I can represent can have only 32 characters. Are we clear on this? Just raise thumbs up. Okay. So that's the biggest limitation of my algorithm.

### 01:50:00

The Admin: But I've not seen words that have more than 32 characters. So this is there and then I figure out how many kind of different characters can be there and that is literally your UTF8. WTF8 can be B C D a smiley for example some sign etc etc which means I can represent anything I want there we clear on this now if I want to represent for example apple a e p l e of my 32 first five are going to be fed as a utf8 whatever bite they have these are coming as a bite inside clear on this but we have to have

The Admin: 8 096 right so basically I had a small weight matrix here not not trained a fixed weight matrix which takes these bytes goes inside and becomes this 896 number right so I have all of these numbers here are we clear then I add my own position emitting here because I know new networks are really bad and I wanted my model to know what spellings are so it's going to be zero for P is going to be one for other P is going to be two for L is going to be three and E is going to be four. So I add my position embeddings also and I collapse that into single 8096 number. So I add all of them and I divide by the total number of actual characters I had to normalize them. That's all I did. So every single character becomes its own dimension. I have America. So A M E R I CA. I add positionings to all of them.

The Admin: I figure out the 896 number for America. How do I do that? I look at the UTF8 byte exact bite for UTF8 multiply that with a random matrix that I have because this is deterministic because the matrix is fixed and I have to use the same matrix till the end of the time because the matrix is comes in becomes 8096\. I have all of them. I add the position embeddings and I collapse all of them. which means I have a fixed method of creating the embedding for any single word that I'm interested in. And this comes back from the fact that the task of the first few layers anyways is to convert the token embedding into the actual meaning of what the word is. So the task for my first layer is much more complicated compared to the task of other first layers because in the other first layer the embedding has stored the meaning. But as you learn more as you look at more research papers you're going to see that the meaning anyways change because there are spelling mistakes.

The Admin: Have never been seen. There are tokens that are use out of context. And when I talk to my claw code, I can see not even single word has a correct spelling. Now everything is slightly weird and twisted. Right? So the meaning anyways has to change. why am I forcing my embedding layer to save it? Why can't I keep it deterministic? So every time Apple comes in, it has exactly the same identifier of 8096 number that goes in first layer that looks at different words and converts that into the actual meaning of apple and then takes it inside. Now because of this what happens is my trainable parameter dropped down to a very very low number because I now have to okay I missed one thing.

The Admin: So normally what we'll have we have 131072 cross 8096 table right we'll have this table and here is the word apple stored and it is some 8096 number in my case what am I doing I'm looking at a formula literally fx which takes apple and generates this fixed 8096 you can come up with

The Admin: many different ways of doing it and so I'm not going into exact interpretation but what I did exactly as I explained a ple e for every single character I determined at 8096 add the position to them and add them that is a fixed representation of how apple will generate so every time apple goes in exactly the same 896 number will come out but I don't feed this to the model I add one more layer of 8096 cross 8096 this is a small neural network that I want to learn what the embedding is for the apple. It will become the 8096 number that this was actually feeding out. So this layer is the only trainable network or a trainable layer in the chronog. So a random fixed representation of every single word goes in but comes out as what neural network wants to learn. This is what comes out right.

The Admin: So I have the training part but instead of now storing around a billion parameter I'm storing 66 64 million parameter and that is what this guy is explaining right. So in the chronocer we are training we have train there are many benefits of chroner embedding for example so if you see training and trainer initial bites are going to be similar you see that the first few model is inherently capable of looking at the characters not possible in case of other model because in other model you're already sending some number right model never sees the spelling of apple or cat or I was not able to finally prove this concurrently

### 01:55:00

The Admin: that this is actually possible. in some tests I couldn't. So this V5 will try to go deeper and see where can we actually send the spelling and there's one big issue I have with the current LM architecture. There's no way a model It just looks at some number right if I say you 4 tell you 47 it is supposed to mean moon but I've never seen m so the inherent structure of how the language is built or the words are built is never actually shown to the model. Right? So this is what is sent. So that's a good Bad part unfortunately characters in Hindi and Indic languages need three bytes not one. And how many said I can represent? 32\. So for Hindi I can represent at max 10 characters. This is a lot but big words like load gamin which is the meaning of train cannot go in. So that is a fallback I have and that is where some of the assignments are going to be.

The Admin: The idea was very simple that I'm going to convert that into fix presentation and have a very small trainable model inside my model which is going to learn and save around a billion parameter and that much RAM is 16x RAM for the model and this is one of the main thing that allowed us to fit the whole 120B model onto a single cluster okay Did you take me one?

Deepjyoti Saha: Aside from my mistake.

Syed Abdul: So based on the explanation there was no need for 32, right? You could have had 128 characters and also since it's a matrix instead of making 8096 at that FX output as 8096 it could have been

The Admin: No. One second. So there's a reason that 32\.

The Admin: So if you do 8096 divide by 32, you're going to see 25 53 right now we have something like 256 bytes that are required to represent. So there's a mathematical problem in doing that. If I don't do 32, if I go with 64, then this number is going to be 16,000. This number directly affects this number. it's not linked in here but I have to make the depth higher which is a bigger cost because if the model goes from 8k to 16k if I want to go from 32 to 64k then there's a lot that has to compress the other solution is that do still do 16k to 8k that additional 64 I'm talking about here I can compress more but this is the main layer where the things are learned so I didn't want to compress here so more thought is required so there's or no answer to you this can increase yes but this affects

The Admin: the D model which is very expensive correct no you need that representation that bandwidth right I can't choke the bandwidth ask 100 it's like…

Syed Abdul: Yeah. Even your FX output is 8096\.

Syed Abdul: So your matrix is 8096 into 8096, right? Why is the input 8096? It could have been just maybe 100\. So it could be 100 into 8096\. No. But those 8096 input is just always a fixed deterministic input.

The Admin: if I send you a cross 100 image and ask you to convert that in 4K not possible the detail has to be there to compress it to expand No,…

Syed Abdul: 

Syed Abdul: So it's not going to learn. The only thing which is learning is that the matrix

The Admin: you're not getting That okay, it's not learned. My input emitting is not learned, but it is a something. You're saying If I compress the representation of the alphabets that are going in, then There's not much to expand.

The Admin: What I've done is what the model would have learned anyways I have encoded that into a fixed algorithm…

Syed Abdul: Okay.

The Admin: which means every word will have a richer description of what it is and there are a lot of words there a lot of tokens if I compress that just to 100 the rep the presentation false automatically yeah so Two.

Sachin Bharadwaj: Yeah, won't the small learning adapter that you placed at cross 8K after FX if you remove it won't the first few layers anyway it implicitly

The Admin: two reasons. In our V4 model, The D model dimension was not 8K, it was So, I had to add a cross 4 because I was at 8K. Are we clear on that?

Sachin Bharadwaj: Yeah. Yeah.

The Admin: Second, yes, we can let the model layer number one learn it, but layer number one is expensive.

The Admin: Layer number one is the transform block and the 66 million compared to 120 billion parameters is literally few%. It makes sense to allow something that can modulate it or form it and the cost of adding a layer as I said if I think there's a problem which I think here it is because my 8096 are fixed number what the model needs something different I can add a new network there but I've followed the principle I told you allow the model to not use it.

### 02:00:00

The Admin: So if the model thinks that this 809 is good enough for me, it will create an identity. It will take it and give exactly the same thing back. So I have basically fixed my problem. New network decides to use it or not. Exactly.

Sachin Bharadwaj: We have a resolute part.

Sachin Bharadwaj: Okay. Thanks.

The Admin: Okay. Nathan. Yeah.

NITIN YADAV: So Rohan you are saying that you are breaking at the character level a b. So are you talking about the token even if we have a token so there also we are breaking it as a character level.

The Admin: So I take a 32 character bucket and fill it with characters. t e. only three are there. Unfortunately 29 are empty. And I fix that by normalizing finally.

NITIN YADAV: Okay. Okay.

The Admin: There are many benefits that are not proven but my hunch is that I can prove it in this time. First of all the cost depends on the vocabulary. It's very small. Second is unseen tokens will work.

The Admin: If I do a spelling mistake for example let's say I send this right this supposed to mean America for example I can tokenize this as a single token tick token can't no other tokenizer in the world can convert a word not seen into sing into a single token but because we can take any 32 character put inside a bucket and get a deterministic output for that and we can still send as a single token that is the biggest benefit and I could have only proven if the model was trained and finally we could have used it in inferencing

The Admin: never had that kind of time. Do you understand the meaning of this? We can drop the to amount of tokens tremendously. In fact, there are benefits that I explored a small model scale. I explored them at 131 million parameter but could not explain or explain the bigger one. Can the America? So, do you realize I can send all this a single token? That is brilliant because I've still not consumed 32 tokens. I hope. Let's see. 1 2 3 4 5 6 7 8 2 characters. And this in our tokenizer can go as a single.

The Admin: So there are massive benefits that are yet to be explored and that is where I am keen on it and Performance was exactly as I was expecting at the end of the model. The predictions were really good…

NITIN YADAV: So I have a doubt so

The Admin: but I didn't get time to check all of this. This is why I feel that at least for me this is one of my biggest invention ever which I've not So has to be pro line please. Bali just raise your hand.

Balaji Chunduri: There's no need for even the vocabulary size like 131k into 32\.

The Admin: Bali no no no no no there is an assignment I'll explain the assignment okay Raj

Raj H: Okay, you covered it. But I wanted to say what happens if you do a typo apple. We put one L instead of one. Yeah. And you could explain is…

The Admin: Yeah, I didn't get your question.

Raj H: how does it behave when we say another fivelet word say Rohal. So could you differentiate between two and how does it become 896? You're saying you want to make it as 8096, right? So, how do we

The Admin: How do we each character has a bite in UTF? I take that bite into a fixed matrix and becomes 8096\. Yes. No. Raj. Okay. Correct.

Abishek Ajai Satnur: Hey Roan, you said that you hadn't been able to prove the chronicer embeddings as much as you would have liked. what exactly did you mean by that?

Abishek Ajai Satnur: What proofs are still left?

The Admin: the things I'm claiming okay so here is on the lightning you can go and…

The Admin: check all I've written a very detailed understanding of what chroner is but on the bottom you're seeing for example kubernetes has this as output and then we have tensorflow this as the output then we have a synchronity this has output so every single word becomes a fixed but you can see that in the 38 positions I'm able to use

The Admin: only few of them but the moment we go to namaste you can see that Hindi because they are using a bigger UTF each character is three bytes I've consumed a lot of that already but look at lightning there is no tokenizer in the world that can tokenize that this is a single token but we can because this is what our tokenizer provides right so namaste is long all the Hindi ones are long you can see that this is where in the bite UTF comparison this is where it falls but every single in fact you can make something of your own for example A PF LE right this is how this token goes. So you can create a token of anything you want. Apple there's a compare to tokens AF

### 02:05:00

The Admin: This is a separation. So doesn't matter what you make it goes inside. and the point is the task of neural network is to take the token and add the context to it and make it a new token. And I keep hearing this for example Mahindra Singh Dhoni is like a tiger. He crawls on the ground. he hunts for the wickets. He runs amazingly fast. Right? And he's the king of the jungle. here the meaning of tiger has suddenly changed to Maid Singh Dhoni. and with all the properties that are there and it is a task of neural network inside the model to add that feature into that token. So that is what I separated I separated the construction of token to something that is deterministic. Every single token will always get exactly the same 8096 dimension. I don't have to learn that 1 billion parameter matrix and then add something that sits on top and let the model decide what do we do with this 8096\. Right? So play around with this and you'll see that huge number of parameters were saved just by using the chroner.

The Admin: So whole of the matrix I had 256 loss 256 and 32 position ones around 66,560 non-trainable matrix is all…

Abishek Ajai Satnur: What? Okay.

The Admin: what I needed and then as I told you that I converted at 8192 into 4096 vector then we have a session I will come to it answer is no unfortunately and…

Sachin Bharadwaj: on the output side it's invertible right I mean you do exactly the opposite yeah okay

The Admin: that is why I was stuck then we would be doing something magical because then we can predict a token that doesn't exist but I'm stuck there. I will explain that in assignment. one of your assignment can I've tested it at a 121 million parameter level.

Vardhan Walavalkar: Yeah also I mean because you're saying in with this chronicle embedding there is no fixed vocabulary and the tokens are fluid kind of thing right and that okay Okay.

The Admin: I've not tested it as a bigger model because I couldn't finish the training of the model and didn't have time on GPU left. I was poor couldn't test it. I have tested it but it's not conclusive enough. so I couldn't publish it. That's the right way of saying it. I have tested it.

Vardhan Walavalkar: So my question is also that by 8096 which is sitting on top of it to convert it to an actual embedding space. is that sufficient enough to kind of map this fluid tokens into a proper embedding space…

Vardhan Walavalkar: which the model will rely upon?

The Admin: Yeah. Yeah.

The Admin: 100%. 100%.

Vardhan Walavalkar: Okay.

The Admin: 100%. Okay. Sachin Raj.

Raj H: Could we use a spell checker before this training or could we use something like find a frequently repeated words like it would find the United States of America in the context and…

The Admin: And do what?

Raj H: then use it for your tokenizer.

The Admin: We can do that…

Raj H: So that f\*\*\*.

The Admin: but those are hardness problems but we have not tested them not related to model But guessing.

NITIN YADAV: Ro what is the inspiration for how we get the fixed matrix with which we are multiplying the character thing.

The Admin: What is the inspiration of this?

NITIN YADAV: No from where you concluded that okay these are the fixed matrix which I'll multiply the bike thing

The Admin: That's the wrong question. I'll so not inspiration. I had few questions.

The Admin: question is right now do not see the spelling of a character or a word that is going in problem number one that I have second problem I have because it doesn't see the spelling it actually doesn't know about what is 69 what is 96 what is the meaning of these things right somehow it has to convert that into some other number third is that sometimes New Delhi always come together why can't I represent a single thing right sometimes we do a spelling mistake I know that AF is not the right spelling But what if I can still send as a single token. So the multiple problems that I saw that were there. Then what I saw is all the neural network paper claim something. They say that we have coming here. The task of the first few layers is to convert that embedding into The actual meaning of things. So this translation happens there. After a logic is worked on and then The meaning is converted into a token that we predict.

The Admin: So if this layer is actually doing most of the work, why can't this be a fixed deterministic thing and from there solve all the properties. So this is the problem and this was a thought process.

NITIN YADAV: Okay, thank

### 02:10:00

The Admin: Okay, moving forward. here's a further more description of how things were calculated and you can play around and see that what is the position dimension. I use 32 as I said what is the D model that is inside what changes parameter changes if the vocabulary size changes then how big are we but over overall formulation is very simple so we have previous one then we go next and then restart very very simple calculation I'll not spend time on that this is the problem that exists in the chrono embedding as of now and the problem is that all the index scripts

The Admin: Unfortunately because we didn't write it, we are the last. A B CDE E took the first few UTF bytes and we came when only three bytes were left. So as I was showing in the lightning one also every single one I use bigger one right. What do I mean? If I use namast example, if I just write this, you can see how many bytes I use just to represent na compared to n. Right? That's blue is n is these many. So that's a problem which means that I can't represent more than 10 characters. So we need a solution for that. And the same thing is explained

The Admin: If I use antastrian right this is internationalization. So if I use that you'll see that I've lost a lot. I have to represent that using two bytes in In fact unfortunately chroner just cuts it. If internationalization is going in and I'm using chronoker embedding it will cut it. It will not even send the whole andas current. That's the biggest drawback that is there because I cannot represent it. Right? So at a token level and current was a token I would have lost it. So the way I handle it by is making sure that I'm calculating when I'm working on the tokenizer that there's no word in indic that needs more than 32 bytes. Right? That is one of the very interesting requirements we had when we made our tokenizer. Are we clear on this? Okay.

The Admin: So if we are going to be using a chronoc tokenizer we need to make sure that when we are covering indic words we remember that those words cannot use more than 32 bytes in the UTF8 representation. Inalization is fine tokenization is fine but all of these are not fine. So for that I have to increase and then I can handle more but the overall size of few things change and…

The Admin: we can explore them. Raj we'll discuss ingredients later on we can do that…

Raj H: What if we write the Hindi word in English and…

Raj H: send it?

The Admin: but that's not what indic okay this is a scar and this happened and we saw it and then we realized damn there's a big issue that is happening and we should have handled it now if you see what is happening

The Admin: Chrono is we have a fixed matrix that determines a meaning of apple and other things right and then I have this cross 8k neural network that converts that into something that a model can ingest if I change my data bucket very fast let's say not math if I go from simple English where single simple words are being used so that cross 8k is getting trained suddenly if I go from there to a phd level English where suddenly the new tokens are

The Admin: getting involved this cross 8K gets a shock suddenly I was listening to Donald Trump all day long and suddenly there's Sashi Suru who speaking so there are words that are coming in I'm getting confused man what is happening I've never heard of these words that cross 8K gets a shock and that shock was represented in the spikes that I saw so if the mixture shift happens very fast that spike is something that we need to handle and this is not only true for us it's true for the rest of the layers also but I noticed that 8 cross 8k was sort of a bottleneck where this had to be handled properly which means that we have to introduce a bit of warm-up steps and this is the right way to train also and learning rate also needs to be adjusted based on the model and other things we have but we need to remember that we cannot just have a no warm-ups and we change our schedule immediately right though.

The Admin: What we have discussed already the curriculum that we have curriculum has to change slowly over a period of time. If the curriculum changes slowly and we have a warm-up stage also then there's nothing that can hurt us and of course the learning rate has to be low when we are training it and high as we change it speed is different ways of looking at and this is by the way a random graph so don't link it to actual training. Raj, do you have a question?

Raj H: No. god.

The Admin: Seth warm up is any link like…

Syed Abdul: Sorry. what do we do in warm up?

The Admin: how slowly are we changing it? So I have a normal English and converting that to English. So how many do I immediately switch the training tokens or do I do in a ratio changing?

### 02:15:00

Syed Abdul: So that is mixture shift like how quickly are we changing the…

The Admin: So if I change quickly then there's a big jump. If I change it slowly then it's better for the model.

Syed Abdul: 

Syed Abdul: how do Okay. So it's like from one data source we bring small sample into the batch.

The Admin: Yes. Small and then slowly change the ratios of course.

Syed Abdul: So that all should be decided before itself in the data ledger. But how would we know? Since you have already experienced it. Okay. Sure.

The Admin: By then tokeniz and…

Vardhan Walavalkar: So Ron actually so in this case there is concept of a subord tokenization and audit what you do in BP by parent coding kind of thing. So okay okay okay okay thanks

The Admin: embedding chroner is an embedding you're confusing with tokenizer whatever tokenizer sends this guy is going to convert that into embedding the position thing I told you that new networks not know the United States of America

The Admin: it doesn't know any of the difference. So we need to add some position to it. So the transformer does not read a sequence. It reads a set. Everything goes at once. So we need to somehow add these positions to the words. And the way we do do that is by basically adding an absolute table. There are many ways of doing it. And one of the way for example is mentioned here. Position families. One of the way is absolute learned which means that I determine how do I represent them. there's a math behind it. So that is something we'll cover in the next session. So absolute learned basically we have a input embedding position enters here. Store parameters one per position and something that we learn. Then we have sinosal which is fixed a mathematical algorithm that we use to define all these positions. Then we have a rope family which is going to be very interesting moment I explain the sections I just dropped.

The Admin: And then we have alibi the one more family that works with it. So there are four different kind of families that we can use. So I need to mention position of where the character is. Right? So that means I have a sequence of texts and I need to say 1 2 3 4 5 6 7 blah blah blah 4096\. Are we clear? Some way of doing it. I can make use math sinosal thing. I can absolute learn from the neural network. In the learned one, we have a normal one. Then we have rope and we have alibi. Are we clear? Yes or no? Okay. So, let's say math or learned one.

The Admin: We trained our new network till 4096\. I mean I'm sending 4097\. What will happen? Model has never seen 4097\. Model is going to say what happened?

Abishek Ajai Satnur: and discard

The Admin: I've always seen 4,96 positions and now you're sending 4097 and then you're sending 5,000 then 5,0001 or 5,0002. Do you realize the problem? Model can't discard. You have sent to the Model is supposed to look at it and do something. And model has never seen this position. Are we clear on this? That is why when we say the model context length is 1,28K. We have to show those numbers or those positions before we can say the model can handle the context. Okay.

The Admin: The problem in this and this is that first of all it ends and then there's nothing that is seen after that and the way these are determined the positions at a later number are very weak to even differentiate between right that is where the requirement was there for the rope and aliy these are the things that are slightly more accurate they can give a better representation or better resolution of the numbers that are bigger so when we discuss about rope and other things we'll discuss that particular part okay so here we have trained from position

The Admin: 0 to 7 and the training steps are 400\. So our loss is going to look something like this. Right? if we increase the training steps of course we'll see different kind of losses. The learning rate is also going to affect it and if we increase the overall positions we're going to see that these are the positions that are never learned. So we have to increase the positions also as we learn. But as we increase the positions total in the network the learning rate also drops. This is just a C2 randomly showed. 14 and 15 I never seen. So you can not expect that if you send 14 and 15 to this model it will actually behave We have no idea. Doesn't matter how much you try. Those numbers are never going to be learned. Doesn't matter how much we change the learning rate. Those numbers are never going to be touched. So we have a problem. You have to train it. If you say that 1 million is a context, you have to train it on 1 million text.

### 02:20:00

The Admin: Okay. All Absolute land are something that we learn in network And they are input embedding table and we can learn as we're learning but again very similar to input embedding and then thereosal we determine and then we send it to the network rotary is important and I want you to see here ting absolute learn goes in the input embedding stalle also goes with the input embedding which means that I have to have a table very similar to input emitting what we were discussing 131072 cross 8096 I have to have that

The Admin: big table because at not 1013 1 072 let's say I have 1 million context lens I have to have 1 million times 8096 big table I have to maintain in both the cases are we clear on this for 4 4,000 position 4,000 is one hot vector 48096 for 1 million 1 million 8096 are we clear on this mistake

Syed Abdul: But for cenocidal it's deterministic growth. There's no learned.

The Admin: But I have to have that number. But as you go forward in order, you'll see that we actually lose this and as you can see that as you're going further and further there's really anything to differentiate. So the frequency drops so little that you can't actually differentiate them much. So cyanos is not expandable. It's good for small sequences but longer doesn't work. the logic is both of them are at the input embedding. But look at where Rope goes in the attention directly. Rope is not sent with the position embedding. So most of the graph that we see for example if you look at attention mechanism or attention model or here example right here you see position encoding. This is old obsolete.

The Admin: Nobody uses This is one of the oldest days in which positioning encoding used to be either absolute learned or assign. Nobody uses this. The new method is rope and rope directly goes inside the attention score. So if you now look at rope embedding today is the introduction of rope embedding. You're not supposed to understand how it works. So do not even bother thinking I am not understanding what is this rope and all. So embedding one of the strokes.

The Admin: Okay, there doesn't seem to be a single. Yeah, here it is. But it will confuse you more but you can see attention query and here we have this rope the top R thing that is mentioned. So this is not rope we remove that and rope we added this may be able to explain. Yes here you can see position embedding rope is added to the mask group query So only in attention layer it is used.

The Admin: So it's cheaper, it's faster also, And attention and then we have attention bias the alibi that goes directly in the soft max and output. So that is even cheaper. So we'll discuss these variants as we discuss more about the architecture. We just need to know that these exist. So in the V5 we have to decide the vocabulary. We have to decide the input path. We have to decide the projection is trainable 8K \+ 8K or 16K cross 8K. The output head is untied. That is the decision we're making because we're making a bigger model. The bite window is architectural parameter. We need to figure out we're going to be 32 or 64 or what because we need to take care of the index and the position policy. Where exactly are we going to add it? We're going to decide that in the next session. We're going to use rope or alibi and where exactly we're going to plug in. These are the decisions required even before we talk about the model architecture. Right? So these are things that we need to keep in mind. play around with this not required. I want to jump to the assignment. Here is my favorite part. I was waiting for this to explain to you.

The Admin: this is something I've been struggling for the last two years right and I want you to think on it and figure out whether you can solve this for me if you can then we both will write a paper and you can write your paper alone without taking my name and keep me out of loop as all the other people do completely fine I'm okay if you want to do on your own but I'll be happy if you write it with me and tell me if you have a solution for this now this is an interesting one and you can help me write a paper along with you this is a direction I'm planning to write a chron

### 02:25:00

The Admin: conquer we do anyways okay and these are the ideas you can pick any of them so there are five of them you can think ponder and work with the agent and suggest what you would do I'm stating the problems there and you can work out your own solution you somehow need to prove that this works and to prove you need to train a model and do something that your agent can take care don't worry on that it will write a data set the model layer everything you need to think with the agent how will you solve these particular problems so problem number one what if embedding can store the mathematical structure what if the embedding

The Admin: of 9 actually had somewhere physically nine mentioned there literally the embedding of nine or the weight of nine and if I do 9 \+ 9 the sum of the two embeddings actually is 18 if you can do something like that then the physical meaning of things can be stored in the emitting right what is the meaning of plus if you can store that and we do 9 \+ 9 if you keep adding if it's a multiplier and it automatically multiplies right if you can do that then you can store the mathematical meaning in the word itself and that's a massive improvement for understanding maths and physics because then a direction vector can save a meaning that means direction right or conjugate can store a meaning of conjugate so can it be possible

The Admin: Think about it. The second is a natural extension of chronoker. So I am able to store five characters in the 32 bucket. Can we do it for the images and audio? Is there a way in which we can use the same emitting for images and audio? Then we can use all the three modalities and send the same time to the model. Of course we may need to an take a patch out and convert that into representation. But is there a way of combining the images and videos and audio and text together and create one singular embedding which can hold this multimodality and we can send to the model. So think about that. Can you solve that problem? All five are different. Don't Pick only one that you want to solve. Now the chrona is limiting with the representation of 32 positions for every word. So apple and a will still take 32 places. There's a waste of space. What can we do here? Can it be dynamic?

The Admin: Can we not send the whole 32? Is there a way of storing or saving that? Or what do we do for the indic? I've not me mentioned that but expand this. What can we do with How can we represent the bigger word in a smaller space because that has a big effect on how the language is processed. Now the chroner is actually a sub idea. I'll actually use the word substandard idea. My first idea was a 4y year. I love foryear. I don't know for year how much you'll know if you start learning about fory year you'll fall in love with this foryear for your year animation I just love this concept of for such a beautiful thing that I can't even explain go for tools type let's go for gif righters can be used for representing literally anything like look

The Admin: this thing it will draw what it's drawing Sherlock Holmes right and this is just a collection of simple frequencies so is it possible to do what I did in the space of 4 year that's a very beautiful way of and that is what I started with I couldn't solve that so I ended up with chronoker and that's why everything is random so my question is that is it possible to treat every single character as some sort of 4 year wave and then add all of them and actually say this is happening.

The Admin: So it's actually a 4 year is fast. We have accelerated for that and neural networks understand for year magically for some reason. If you somehow can send for a signal to neural network inside the model it can immediately expand it right there magical thing that LM can do and neural networks can do. But the question is it possible to convert this into proper 4year signal and this is one of the question that other person also asked. Unfortunately, my for embedding is It is not reversible. Right? And I've been banging my head on how do I make it reversible?

The Admin: What is the meaning of Reversibility means that any token can convert into this deterministic 8096\. Can I take 8096 and convert it back into the tokens? Answer is yes. But neural network does not predict exactly those 8096 numbers we want. What I mean with that I will not draw 8096\. So I will say apple let's say gets converted into 0.3 0.2 0.1 uh 0.2 0.3 and 0.6 neural network does not predict that neural network will predict 0.31 0.18 0.09 0.0 uh 018 then 0.29

### 02:30:00

The Admin: 29 and 0.58 and after it gets extremely well train Initially getting these numbers when the model is random and training is not even possible. It's impossible. So we can't even predict a word. and after it gets trained it might get close to the final numbers it predicts. So it's a big problem. and this They're very close but they're not same. So how do we make it invertible? Because if you can make it invertible then we can force a neural network to predict a 32 character span at once. We can speed up neural network or anything. There are some directions that I have. I have not explored them. One is called KL divergence and basically this is used in VAE variation autoenccoder. the logic very simple and this something if you learn you'll be super happy. We do not predict a point.

The Admin: we predict x plus some gshian distribution. So I'm going to use let's say delta. So what we say is that not this not 0.1 but 0.1 plus minus 0.05 for example then you're predicting a point cloud. So if this concept can be introduced then those two variances can be handled properly and then you can predict that okay you actually predicted apple. So the last problem that I have on this is how do I make it deterministic in the reverse order. If you can do that done we are going to be solving some of the biggest problems in there and then we can start raise a billion dollar and then move to London and then stay there and then forget everything. So pick any of these problems submit a solution your solution do not only pick one of the problem that you have. Prove that your solution works.

The Admin: to prove how your solution works, your agent can help you. I need a good read me where I can see if you want to make a web app, not a problem. But a boring read me which tells exactly what you're doing is good enough. And then you need to get your agent to take that train a small network and prove that the whole thing works. So you're submitting code and you're mit read me done. Okay. Rahul.

NITIN YADAV: Yeah, So I have a basic thought. I know that you have tried that but I just want to know the drawbacks of that thing that you are mentioning that you want to have so why are we not checking the cosine similarity between the vectors to just predict the most nearest one.

The Admin: not doesn't work at cosine similarity works when vectors are very close when the model is random initially nothing will come close and we want the model to at least start getting to train the point is that once the model is trained we can think of something how do we do it at random state the cosign similarity will be and…

The Admin: cosign similarity does not work in low dimension is fine so you'll say okay why don't we do tney which works in high dimension the answer there is that initial randomness is so much that the vectors are very far apart.

NITIN YADAV: Mhm. Okay.

NITIN YADAV: Thank you.

The Admin: Okay, Praish

Pranabesh Dash: U so you are asking the students to use agents to solve this problem. So I had just read something recently that using AI there is a part intelligence is part judgment and agent can do the intelligence part and as models getting better they can do that. and also it said that with time agents will be able to do the judgment for you. So whatever you are asking here do you see in the next year V5 whatever you are asking students to do that AI will be able to do in the next version.

The Admin: Of course, even I think it can do today. If you run something like what Karpati did auto research, it can solve this problem. But that means that one of you is spending around $200 or $300 on cloud for four five days.

Pranabesh Dash: Okay. Got it.

The Admin: Have we check these faster four solves one 2 3 automatically and…

Abishek Ajai Satnur: Rohan, if you had to pick which problem is most relevant right now to the five problems you listed, which would you say is the most relevant? the last one. Okay. Okay.

The Admin: So problem number four solves 1 2 and three. Problem number five solves completely different problem.

The Admin: These are the hardest…

The Admin: but unless we solve one two and three I don't think we can solve four and five. So there's a sequence also. Okay Sachin.

Abishek Ajai Satnur: Okay, thank you.

Sachin Bharadwaj: So Ron in the previous version you had output head that you trained separately along with the chronicer.

The Admin: Yes. the factorization is chronical factorization.

Sachin Bharadwaj: And why do we call it chronicle just because is there a reason to name it chronicle?

### 02:35:00

The Admin: So 10 into 2 and 2 into 10 is equal to 10 into 10 is a chronical factorization. That's what I did So my thing takes 1 13 0 72 into something and then something becomes what the model needs factorization. Yeah, these are the problems that are there in my life. If you solve these then they will be less

The Admin: problems left in the life. I forgot one very important thing. I've updated the session before the pytor basics and I would like you to go through it. this is a read not in the class and the reason is that pytor is required but now everything is going to be coded by LLM. So I don't know how much of it you need to know but you still need to know what is a tensor, what is the module, what is the forward loss, backward, how does it look like at least in the code then what are the tensor shapes and other stuff. So just play around and see what these are. and these are things that you are supposed to know. If this was 2024, I would have spent one full session on this. Today it doesn't matter. You will not even look at this. But in an interview people might ask you or you may need to know few things and when you look at the code it might cla what do you think we should do about the backward call and if you don't know what it means and you'll see what do you mean by backward call or if it says that autograd is not enabled on this parameter you need to know what does it mean right?

The Admin: should do a quick read on what this is and you'll be good to go. All right, this is where the session ends. I'm going to stop the recording. If you have any question then please keep it coming. So on answer is we have to train on it looking at the United States of America.

Soma Korada: Again I'm getting a little confused. So if we are saying the United States of America can be one token based on chronical embedding. are we saying that the tokenizer which we're going to build for the model which we going to build is not going to follow the PP tokenizer or any of those patterns but come up with a new strategy to build the tokens. Got it.

The Admin: We have to figure out a way in which the tokenizer does its job. But there's something that sits on top of tokenizer and does these smart optimizations. So we have to write that optimization thing. We have not done that yet.

Soma Korada: Because otherwise we will not be able to use optimally the chronicle embedding if the spelling mistakes.

### Meeting ended after 02:37:24 👋

*This editable transcript was computer generated and might contain errors. People can also change the text after it was created.*

