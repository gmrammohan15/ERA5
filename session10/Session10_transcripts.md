## **ERA V5 Session \- 2026/08/29 06:44 IST \- Transcript**

# **Transcript**

The Admin: All right, let's start a recording and good morning everyone. Today we are going to be looking at probably one of the last pieces of training which is going to help us stitch a whole program together. these are things that are also super important from the point of view of training and monitoring training for weeks and probably months if time allows us. some of these things we have already discussed but we'll discuss as a cursory glance. today we have the u time and moment to actually go through each one of the concept that we test upon. So till session 9 what we've done is that we've said that we have a token that is going to be converted into embedding and then finally it will be somehow converted into loss.

The Admin: So today's session is figure out how is it converted into loss and what does it mean for a computer to calculate loss or GPU to calculate loss and how can we speed that part up right because there are levels of accuracy we are okay with and anyways initially when we train the model we have a very noisy readings that are coming in so it's very difficult to say that would it make sense to calculate everything with extreme precision would mean at least

The Admin: float 64 you may have heard of remember the era from where the operating systems were at 32 and from there they went to 64 right so the same concept we are going to be discussing today so as of now what we discuss is we have a token coming in or tokens coming in so there's a sentence there's a great news out there for example that token sentence is coming in that is going to be sent to the model and it's going to predict the next token however remember as I told you that if 10 tokens enter the model 10 tokens

The Admin: will come out. So if 1 to 10 enter the model, 2 to 11 is what is going to come out and that cannot stop every time that happens again and that is converted into logits. Logit's going to be The prediction head saying that I think Delhi by 4.5 or Kolkata by 4.0 or Mumbai by 3.4 and so on. That peak number that we get out the output that we get that we feed to softmax. after that we fed with softmax or finally we have our loss number calculated. So this is what we're going to be discussing today. How's the converant loss and how do we take it from there and how do we update our models or the parameters that we have. Right?

The Admin: So the embedding head that we have is going to be something like half a billion parameter depending on the vocabulary is and how large dimensions are and after that we have several billion parameters inside the model itself. So the input embeddings are going to go inside. There's some multiplications happening. And finally we have one number that comes out that is a loss right so that is the interesting thing what is this one number and how do we understand what about things about this number and how do we make sure that we actually training right so we'll launch our GPU with the model is running how do we know it's actually training properly what are some of the KPIs or some of the key things that we can monitor to understand a model is actually on the right track so this graph you have seen earlier this

The Admin: overall widget. What we understood from this one is let's say we have a Zed is the final value that we want. We're trying to solve an equation. that is a multiplication of x1 which is input that is coming in. There's an input that is coming in. Then we have x2 which is another input that is coming in. any input that we have for example a token is an input. We just don't send it to the loss. We have some weights that are going to be multiplying with them. In our case the things are very different.

The Admin: This is the first session widget that I'm using. Just to recall, we have this W1 and then We have this W1 and then we have this W2. So as we train the model, the task of the neural network is to make A function is a surface. Think of it like that. It's a mapping thing. So when we map everything and we can map every single thing, it becomes some sort of a surface.

The Admin: in 2D is going to look like a plane in 3D it's going to look like some 3D geometry 4D and on which we can't think and unfortunately our models are working in billions of dimensions so we can't even imagine what is happening there but if you can visualize sort of a mapping function so a new network is trying to map all the points that we have it's like conversion from a point cloud to a 3D model right a point cloud will look like a LAR output for instance the sort of a point cloud right and neural network is trying to make a geometry around it. point cloud is going to give you some points right not all the points are there.

### 00:05:00

The Admin: If every single point was there then we have the model already ready the function that can define it properly but we'll have holes somewhere we'll have gaps somewhere and that is a task on network to fill up that is what learning is because if everything is already mapped then we do not need but the point is that our data set or everything is not there precisely exactly as we want right for example a simple question how much cricket is such a tender it's a very weird question but you can actually answer it or how much cricket is ti now or how much cricket is let's So in this case you have to rank them from 1 to 10\. It's a question I ask. must exist. You can ask this kind of question to network and it's supposed to answer So not everything actually has the full surface and that is why we get this kind of point cloud and that is the data that we feeding. The task on network is to map some surface or some geometry around it. Very easy to understand when we're looking at a 2D plane. Right? But what is happening here is the weights are changing. So the blue one and

The Admin: able to try and convert themselves using some back propagation and loss which we'll talk today into some sort of format where it allows us to map the geometry for x1 and x2 to exactly the number we want. That is what happens during training. In validation we send few more points and see that whether they're sticking to the surface or If not then we know we have validation error. So there are few words that we need to be aware of and these are the words that are going to are used in different ways also. So we need to be aware in what context we using it. For example, if I say bank, what do I mean by bank? You need some context. it's a bank of the road. Similarly, We're going to talk about what gradient actually is. Then we have a step. We have a batch and then we have micro batch.

The Admin: Okay, we are on black only. what you'll see is we have a loss function and that is going to be very simple or the simplest manner it's going to be that we were predicting 000010 0 token but we were given 0.21 0.06 0 7 and then 0.001

The Admin: 001 and the difference between them. So we can do an square difference. We can do element wise linear difference and there are many different ways we can define a loss function. But the logic is that we have the expected outcome. Let's call that y target and then that we are providing as output. The difference in them is going to be the loss for us. But this thing came out from a model, And the model may have some Z here. And that Z may be into X1 plus into Exactly what we saw on top, right? And these are the X1 and X2 input that are going in. So this is how our new network looks like. The gradient here is going to be how much of W1 should be changed, right? The gradient of a gradient is very simple.

The Admin: we have a curve at any point the tangential line there is the gradient right so exactly same same concept the gradient here is what we're talking about is how much of w1 is changing how much of w1 and w2 need to change right for a loss to make sense I have a very simple table down below the logic of gradient is that it's attached to the weight that we have so here we have weight one and weight two so we have two gradients right now here gradient is something that we keep and gradient is and aculate. Gradient is something that we have to flush after every step. All those things we need to discuss.

The Admin: But that's Any question on just the gradient part. These are very simple concepts which will keep on building one on top of other and after that we need to look at the whole world from top and make sense of everything that we'll discuss. Everyone clear on Any question on Gradient is the delta change that needs to be attached with every single weight that we have. All right. second is the step. So if you read here a step is one complete pass of the loop. read some data compute the loss compute every gradient then move to the next weight.

The Admin: So what do we mean by this is imagine that we have a box. We do not know what is inside the box as of now because we'll keep on changing a definition of this box. we have example tokens coming in or some data coming in from this side goes the Model is inside this machine. And after that here we have another same machine but used in a slightly different way where we're going to be calculating all the loss back propagation the weight step all we discussed this is going in this is forward loop this is backward loop and now we are ready for the step number two right so all of this is one single step so when we say that we have taken a step we mean that the model here was updated fully every single weight inside was updated a zero is also an update because we know that there was no update

### 00:10:00

The Admin: for this particular weight as of now but every single weight was touched. This thing is called single step. the reason we're talking about steps is because there was a time when we used to have something called an Epoch would be that I have this full data set and I would like to go through this data set once and that wasn't enough. So in case of convolutional network we'll go through that data set many times. But that's not a concept today. We have enough data set that we can't even cover once or sometimes we'll cover maximum twice of size. So it makes sense to talk about 045 epoch. It doesn't really mean anything. That's why we talk about steps. In how many pieces have I broken my data set? So if the whole data set was something like 1 billion tokens very small but we discussing this because 1 billion token is 1 billion tokens and we discussed in the last session that we like to have a batch size of something like 1 million right. So in 1 million token per batch per step that is per step right.

The Admin: So 1 million here. So now we are clear. Okay, we're talking about thousand steps. so my training is thousand steps. I am on my 45% of training is done. So one step is essentially going through the data once and we doing back propagation. We care on this. So one step equals to x number of forwards plus one back prop. Till now I was saying one back. Now I've changed it to x forward and back. Are we clear? If all of you are clear then you're not even listening.

Manjith Adapa: What is it?

The Admin: X is essentially unknown. It can be Four forward Five forwards. Are you comfortable with one forward and…

The Admin: one backward?

Manjith Adapa: That's in the first case …

Manjith Adapa: if you're doing 1 billion token is it 1,000 F \+ one backward. What? Okay.

The Admin: Something like that. But we'll discuss why when talking about something like that. It's not going to th000 but it's going to be something like probably eight or 16 or some sort of that number. We'll discuss why. but I want you to have this question that I wrote X forwards and one So essentially one backward. That's the simplest thing. we have Sono.

sonu agarwal: is there I mean this X and the optimization also has some relation but how we decide the X and then Okay.

The Admin: Yes. Yes.

The Admin: Okay. Chak exactly that's…

chirag Tagadiya: So one step is like whenever you do first bad progression that means your step is finished can you think like that? Okay. Okay.

The Admin: why I wrote X here. So it can be two, it can be three, it can be eight but one back prop. So one step is equals to one backdrop. That is what we need to correct.

chirag Tagadiya: Yeah. That means x can be multiple for example 4x when you accumulate four times right.

Vardhan Walavalkar: Is this different from a batch? It's

The Admin: No, I'm just waiting for the next slide to explain what Okay. M this X is fixed for all the steps.

M: Is this x fix for all the steps? Okay.

The Admin: 

The Admin: That's And then A batch is a group of samples that we send to our model. what does that means is that let us say we decide that our token or our sample length is going to be 4096 or 4K context, right? We're training for 4K context. how many samples are we sending at the same time? let us say we are going to be sending let's make it interesting that will clear up all the things that we're discussing. Imagine that my target is to hit 1 million

The Admin: 1 million is going to be how many 10,000 10,000 and then 1 million okay but my GPU is small so I can only send thousand at once so that means we have thousand left here okay and let us imagine that S gives me a cluster of 10 GPUs it never gives a cluster of 10 GPUs as 2 4 or eight but I'm keeping calculations very simple right so AWS gives me a cluster

### 00:15:00

The Admin: of 10 GPUs. I need to match my 1 million token per batch as a target but my GPU can only handle thousand. So let's see what is happening what is the Batch size is 1 million tokens. Are we clear on this everyone? Thumbs up. That is the targeted B size that we have right now. we'll move to targeted ch What is the batch size achievable right now? So Microbatch size is how many tokens are there on each GPU? My microbatch size is thousand. We just discuss it here. Each GPU can handle only thousand. Are we clear on what is microbat size? How each GPU can handle? what is my effective batch size right now?

The Admin: which basically means a 10 GPU system that I said I'm going to take from AWS that becomes only 10K clear on this okay so my microbat size is the total number of samples total samp total number of tokens my u or samples my GPU can handle total effective batch size here is how many GPUs I have so if each GPU

The Admin: is handling let's say 10,000 and I have 10 GPUs then I have 100,000 handled there right so right now you can see that I'm only able to handle 10k but I said that I want to handle a million here right so that is where the concept of gradient accumulation comes in but if you quickly do calculate you're going to see that my gradient accumulated steps are 100 how we have 1 million as a target unit 000 10,000,000 million I have 10 GPUs. Each GPU can handle only 1,000 tokens. So 1 2 3 4 1 2 3 4\. So 100 is left. Somehow if I can accumulate gradient for 100 times then I can meet my 1 million target. So we have gradient accumation steps is equals to 100 here. So what will happen is I will send data to my GPU which is going to be now effectively 10,000 tokens at once. My GPU cluster.

The Admin: It's going to calculate the loss. No back prop. I'm going to do that 100 times and then I'm going to do single back prop and weight update. Are we clear on this? I misspoke. I am going to do back prop. Sorry for that. I'm not going to update the loss because I have to save it somewhere. So, I forgot that particular part. So, we're going to do We're going to do backward. But I will not do loss the gradient update. I'm going to store the gradients for that particular step. So, I'm going to save those gradients for 100 steps.

The Admin: Otherwise there's no accumulation. So backward once gradients are calculated do not update and save save the gradients do not third gradients do not update. So do that 100 times and after that we average those 100 and then we have our batch size of 1 million to consider. Any question on this? What we have discussed here is we have a micro batch size.

The Admin: Then we have the batch size that we want to target. We calculate a temporary batch size that we have to figure out how many acclimation steps we need. Then we calculate total acclimation steps. So I'm going to be acclimating my gradient 400 times. I have 10 views and each of you can handle thousand tokens and that effectively give me my 1 million token per batch target. Aish

Avnish Midha: U but Ron aren't we sending different parts of the context and…

Avnish Midha: the gradient that is coming back is it going in the relative. I'm just wondering…

Avnish Midha: if it's going in the place here.

The Admin: So okay one second the easiest part to understand this is that imagine that I am rich and…

The Admin: I can buy 100 of these in that case same examples forward backward calculate correct so instead of this in parallel…

Avnish Midha: Okay.

The Admin: because I don't have money I'm saving them somewhere and then implementing Correct.

Avnish Midha: So they are in their respective con the structure is big but respective area I would say. Yeah. Okay. Okay.

The Admin: Instead of doing it in parallel, because I have money, I'm doing in serial. Of course, I'm going to waste time.

dharshan thaigu: Yeah. the thing is we already have a know the token values but it is based on the effective batch size that is how we can go along with the gradients. So these two values will be predefined and we make the calculation then only we can the gradient So it will changes which the things has been changing which are the things which because token has been predefined already. This is how the token value would be 1 million or 1 billion whatever it is. But what about this effective batch size and how the gradient has been changed based on that these

### 00:20:00

dharshan thaigu: what are the things will be standards we'll predefined and what are the things we can change it in the future if there is any changes Okay.

The Admin: nothing changes…

The Admin: unless we update the gradients. So we just storing the gradients.

dharshan thaigu: Oops. Okay.

The Admin: So let's say we are talking weight one sample one comes in this becomes w1 plus delta W1 right then sample 2 comes in this become W1 plus deltaW1 plus delta W second sample then third sample goes in W1 plus we are not adding always you can see that I'm always maintaining it somewhere else and so on so here we are accumulating the gradients I have not never updated it right so what happens is that for every single weight we have a gradient box where we store

The Admin: the So for one, so we're saying 100 exclamation steps. So let's say this is In the second step, we calculated 0.2.

dharshan thaigu: Okay. Let's

The Admin: So we're going to add that 0.1 and 0.2 becomes 0.3. So we have updated that. so I do not need one more column for that. So keep on we say we accumulating it, right? So 100 times I'm going to accumulate this and finally maybe I have 4.5 divide by 100 steps because I need to average it. Then that's the final gradient that we have.

The Admin: Okay, that didn't not memory thing.

NITIN YADAV: So ro you are saying that we are not updating the weights. So that's exactly we are saying for the memory thing right sorry I don't remember

The Admin: Why do I want to do 1 million tokens? We discussed in last session. Not Why do we want to do 1 million tokens? First step we discussed in the last class. Then why asking question who can answer this? Why do you want to wait for 1 million tokens? Why should a bat size 1 million or a large number? 1 million is what most of the labs follow. We will try at least a half a million.

The Admin: Anyone who knows the answers.

Soma Korada: to optimally use our GPUs.

chirag Tagadiya: Saving title Post.

The Admin: No. No. People who know the answer are writing it.

Rahul Uniyal: Smooth lost.

The Admin: Speak up. Okay, let us say you have 100 people in a room you have invited them for dinner I like you to go to each one of them separately and…

Deepjyoti Saha: Stability of the hand.

Rahul Uniyal: This is smart.

Satyanarayana Murthy Toleti: That is the bad size design.

The Admin: ask them what is it that they like to eat and then make a food for them one Other approach is you stand on the sofa or your table and ask everyone what would you like to eat? Everyone screams and then you hear out the maximum noise and say yeah that sounds like what I want to make right now. If we send one sample to a neural network and ask it to learn for example look at this image looks like a dog the whole model is going to update itself for a dog and tell itself yes I can remember a dog next time you send an image of a dog it's going to get even better and going to say yes I know how to actually predict a dog my loss is dropping then you send a cat and it's going to say it's dog and your model will be told no it's a cat then it's going to say okay so now it's going to start learning how the cat looks another cat example comes in it's going to say yes I know what a cat is then

The Admin: send a dog You're going to say no it's a dog. The model will get confused because never seen cat and dog at the same time. So let's send cat and dog at the same time. If you send cat and dog at the same time but your class also had elephant. It's going to say dog or cat only but now you have sent a photo of elephant. It's going to say cat. You're going to say no it's an elephant. So now it's going to learn about elephant while it's forgetting about cat and dog. We don't want that. And in images at least we had thousand classes. So we can go for a bigger batch and batch size let's say 32 or 256 also because at least in four cycles I can remember them right so I can send and my model can learn. But in text we have billions of tokens right we have different words different combinations used in different context. So if the size is very small the model will not even know the diversity in which a single token can be used.

### 00:25:00

The Admin: And if a big feedback is coming in every every time if the bat size is small every time the feedback is going to be very big because never seen that or it's certainly going to change how it looks about a particular token right so bigger batch size essentially provides a smoother gradient it provides gradient which are smaller it provides sort of an average out context of in a different way in which things can be used that is why we need a bigger bat size and most of the labs use around a million tokens we clear on this we just send 100 tokens is going to learn that

The Admin: And it's a big model right so it needs to update a lot of weights it needs to have a lot of context how all the words are used and all ideally a billion will also work but we do not have a GPU in today that can handle such things right so that's why we want to go for a million token in the batch size that's what labs use we'll see how far we can push our own hardware right again now what we discussed we a weight will have a gradient this is the gradient where we were saving it gradient is how much I want

The Admin: to update in the current step. Right? So this is the weight and then we have a box for it where we're going to be saving or storing with how much gradient we want to update it. Again we have a weight which is four. How much gradient is 0.1. We calculated that using back propagation and we're going to subtract it depending on minus sign that we have there. Right? So it becomes 01 or 3.99 sign is also going to be saved here. But assuming that we have acclimated for millions million tokens. we are poor. So we had only 10,000. So instead of doing every time 10,000 instead of doing 100 accumulations or 100 updates we are going to save it

The Admin: 100 times, right? So becomes it keep on shuffling, But shuffle happens internally and finally whatever the last average value that we have, we're going to update that and finally we'll have our correct token. Right? So again we have something called A micro batch size is how much in a single GPU samples can fit. remember we're talking in terms of tokens here, So what we discuss is that each sample is thousand and we have 10 GPUs and then we have 100 exclamation steps not thousand we have 100 exclamation steps but generally when we are going to be talking about this batch sizes and all we would have already divided by tokens right because it becomes easier so let us say we had 100 tokens per sample right so 100 tokens per samples how many samples we have then 10 right so here you would have set my GPU

The Admin: two micro badge size for one GPU was 10\. Are we clear? Internally we are saying that we have 100 tokens but this is what we like to talk into because that is how we're going to be making our data set will have rows. How many rows are we sending? 10\. Are we clear on this? We can talk about microb size in two forms. How many rows? knowing remembering that for example if you and me are doing some scam and we are sitting in some Mumbai ta and then we are going to discuss in 10 koka right yes or no you have a mustache and then you have a big masa here and we're discussing about the crime and we're going to say kalea and you're going to say 10 koka so we know that we're talking about there you're not going to say kok you get slapped there only right so please keep in

The Admin: So when we say our microbat size is essentially that means 10 samples are coming in and each sample might be 4K 8K 16K depending on what we've agreed on. So this is bat size. bat size is going to be how much money you have. Are you a 8 GPU guy, 16, 32 and so on and so on. Till eight we get one clust one single machine we can get a single machine from AWS. After 8 we get So A cluster of these four becomes 32 and so on. Right? So when we say a b size you're talking about this multiply with this. 32 into 10 is 320\. So you have a bat size of 320\. Remembering that we have in each row 100 tokens there. Are we clear on this? if you know that we are poor and we cannot go with 32 and we have to live with two only. So we start accumulating the gradients.

The Admin: So instead of let's say this is one batch microbatch two ba four microbatch this is the model right so if the whole model could be held in the GPU everything will go at once and we'll get a value here out but we can't do that. So we have one batch going inside the GPU we get something then this was one then two goes inside the same model because if you update the model then we are not following this we can't update the model right and then we get B then we send three then we get C and then we send four and then we get D.

### 00:30:00

The Admin: So how and these are the gradients that are stored inside the gradient was 0.01 here the gradient was 0 01 plus 0.02 remember that right yeah we're adding on top of it and then we have \+ 0.02 02 plus 0.03 zero coming from C step and from something from here maybe negative right and finally is the step using which we are going to be doing the weight update W

The Admin: Then put it. Okay. M.

M: So I just wanted to understand…

The Admin: 

The Admin: Yeah. Go ahead. That is not…

M: when we say one example we'll be sending one token plus two tokens means if the sequence length is 10 we'll be sending 1 \+ 2 \+ 3 like that right so how will this get distributed among the GPUs

The Admin: what we're discussing today. We will discuss that today when we discuss about we actually already discussed it. So we'll discuss again data loader. We had a exercise on assignment also on that. So I think you are a good question.

Swati Bansal: So does the batch size vary depending on the training phase? For example, if you have long context, then we need to have different obviously how larger samples, right? So how does that change over the GPUs or the phases?

The Admin: We train. So let's say this is the sequence length.

The Admin: So 4k they have 8k we have 16k then we have 32 and then we have 256k and then we have 1 million let's say this is a lock scale right now we do not want model to speak gibberish initially right and 4k gibberish is already good enough we do not want a model to do a 256k gibberish because it's all nonsense so here when we are training initially it's all nonsense right so we'll keep our total sequence length All so what you see is that for and these are steps for example this is exactly the training cycle that we need to come up with how

The Admin: How long we want to train on 4K, then how long we want to train on 8K and how long we want to train on 16K and then 32K and then 256K and 1 million 1 million finally. Right? So that's the schedule that we need to come up with. let us say we have the same machine and same model. initially here we want 1 million and let us say I again had We do not get 10 GPUs. We get eight. But keeping my calculations easy. So 1 million is something like this divide by 10\. So this is what I have right imagine that of a 4k this I written as 10\. Okay, it's going to make my calculation complex. So I'm going to raise it again. Okay, so I'm going to say my context length here is going to 100k and then going to 1 million and easier to look at or is going to be,000k.

The Admin: We need to decide how much we want to train on 10k and then there and then from there 1 billionk. let us say I have 10 GPUs and each GPU can handle only let us say 10k 1k okay so my micro batch size is equals to 1k my batch size effective as of now is 1 into 10 is going to be 10k…

The Admin: which means the gradient acclamation steps required is equals

The Admin: to one. I do not need to create an accumulator because I'm matching this with the sequence length that I'm targeting there. Now I change and I do not want to change the machine. That means that I have 10 times more GPUs I don't have.

Swati Bansal: Okay. Yeah.

The Admin: So I'm going to serialize them. Which means my gradient accumation steps here is going to be just equal to 10\. And similarly here it's going to become Of course going to be 10 times slower. And of course this is going to be 100 times slower because I have to wait that long for one single step.

Swati Bansal: Okay.

### 00:35:00

Swati Bansal: So, it does vary depending on which phase of the training you are in. Okay.

The Admin: Exactly what we should not change which we did in our V4 and that was the wrong thing to do and I'll be frank I'm also learning as we do things if we decide that our context length or one single steps length is 1 million token we should not change that.

The Admin: So while different phases are happening we should try and stick to the same thing. initially in our case we were at something like 0.12 million then we went to 0.25 million and then we went to something like 0.49 million I believe or most of the time we were in this range but we did not shuffle because the average changes right suddenly the less information is coming from less tokens certain information coming from more tokens.

Swati Bansal: Got it.

The Admin: So this is noisier this is smoother. but we need to stick to a particular number. Okay.

The Admin: Chug. Yes,…

chirag Tagadiya: So Rohan when you say you're trying for 4K sequence L followed by 8K 16K. so you have to change what do you call in one single batch the length of the token will be like 8k while you're training for 8k then if you're moving to 16k you have to stop the training right and then go for the 16k

The Admin: 

The Admin: of course. And have do You have to train on 4K. You have to train on 16K. Why are you telling me to do it?

chirag Tagadiya: Okay.

The Admin: I have to work. I have to stop training. I have to be careful because I want to take responsibility. When the training happens, everyone just runs away. On the training day, you're going to say no, my left thumb is getting married to someone's right thumb.

chirag Tagadiya: Got it. can you go to the previous slide…

chirag Tagadiya: where you are explaining about red? Yeah.

The Admin: No, these are good.

The Admin: These are drawn on one. This is like a blackboard digital track. I've not added the fe. I'll draw it again. the surname it sounds like some background music will start and then there some deep voice will come right. It looks like stepping down from a big mansion and very serious. Doesn't want to ask contact length is not different from sequence length.

Avnish Midha: you're on is context different from sequence length I believe okay but then when we are upgrading the gradient shouldn't we upgrading updating the different parts of the context in the overall like a okay…

The Admin: No, no, no, no, no. That's a task of backroation to figure out which part of the context I need to update.

Avnish Midha: because we were adding so I was just wondering whether it should add or it should just do it in different parts of the section

The Admin: No, that addition has already taken care of the feedback from all the other tokens. The final number.

Avnish Midha: Okay.

The Admin: Okay, Chag.

chirag Tagadiya: Okay Rahul can you explain …

chirag Tagadiya: how for example we have 10 GPUs right and…

chirag Tagadiya: each microb is giving some gradient how you combine that gradient for the update. Okay. But…

The Admin: Yeah, we save it,…

The Admin: we we add it. So let's say I get 0.01, next time I get 02, I add it and only save 0.03. So I'm accumulating it. That is why the term accumulate.

chirag Tagadiya: but it's for example 10 GPUs are running parallelly. So they will all throw out 10 different values and then you combine that or…

The Admin: Correct. No,…

chirag Tagadiya: or you wait for all the 10 to finish and then send it to the driver or accumulate. okay.

The Admin: everyone has to finish, I can't do midway. Everyone has to finish and everyone will finish at the same time because it's the same number of tokens, same algorithm, same model, everything is same. So all of them will stop at once.

chirag Tagadiya: Please.

The Admin: 

The Admin: 

The Admin: All right. So, we know Microbat size is what s fits inside one big expensive B200. A bat size is what fits inside eight two expensive B200s. A step is us deciding that I want to propagate now. I want to wait for forward backward 10 times and then we won't go back propagation. And radient is what we are accumulating or gradient is what we change our weight with. That's the step number two. All right. where does the gradient come from? this table is weird. So, I wanted to squint into your eyes. Can you squint your eyes? can you look like Okay, how do we fix this? I was thinking of fixing something like this, but I thought I can just scale my screen and then show it to you. So, I'm also lazy. Okay, so imagine that a particular weight somewhere sitting inside a billion parameter model is three, right? And the loss right now is 16\.

The Admin: What actually happens in back propagation is there's something called autograd which we are just going to discuss. It calculates the equation of the rate of change of loss with respect to this weight. If you have a billion parameter now we have drilling parameter models also. The task of the autogradations engine is to calculate the rate of change of loss with respect to every single parameter that we have in the model or So here in this simple table what we're seeing is if the weight was three the loss was 16\. If the weight changed to 3.01 the loss change to 16.064. Is this but clear? This is very easy to do.

### 00:40:00

The Admin: Once you have the equation, you just change the value and you can see how much it's changing. And the calculating equation of loss with respect to every single parameter is the mathematical genius of back propagation or pytorch or tensorflow. This is what exactly they are for. Everything else is But the main thing behind that is autograd which calculates this for Any question on In this table you're seeing that That weight change is 3.01, a loss change to 16.064. Any question on this? Because everything now builds on this. At least do hands up or hands down. That means if I calculate the rate of change of loss, so loss changed to 16.064. So 064 \- 16 is going to be 16 0.064 and my weight changed 0.01.

The Admin: to 64\. Rate change of loss with respect to this weight is 64\. Big number, right? So it tells us two things. If the weight increases, the loss increases and the rate of of loss with respect to this weight is higher. Can you see both the things right now in this very simple table? You're going to say I can't see because I can't see the loss. It is somewhere out there, right? So, let me write it for you. So, as you are 16.064, can you see Don't say the four doesn't look like Right. So, the two things are evident from here. The rate of change of loss with respect to this weight is high. 64 is a big number.

The Admin: And second that it's a positive connotation that if we increase the weight the loss increases. So we should reduce the weight right and that is where the equations and other things come in. So we add a negative in front of it and that tells us what direction we should reduce it. Are we clear on this? So right now the delta L by delta W is 64\. We're going to add the negative in front of it. That's where the equation math comes in. We not going to go in that direction but that's how we know what should we do And the 64 is a big number. The 64 may be coming rightly right only from the current example.

The Admin: 64 may not be looking at the long-term changes or the 64 is for the word like psychopanth psychopy which may only come once in the million token budget that we're also sending in we have billions of tokens and trillions of tokens and lot of different context right so even the gradient is big 64 we do not pass on the whole gradient we take a small piece of it and we provide that as a update right that's where the learning rate will come in we'll have a session dedicated on top of it so learning rate is going to reduce this further but it reduces all the weights

The Admin: sort of in a similar fashion. this is a widget that we have seen earlier also. So, we're just going to spend a little bit of our time on this and then move forward. So, let's reset everything. We have the simple model. Y is equals to relu of wx \+ b. Our data is one that should give two that should give three and three that should give four. So we calculate the first value that we have x goes equal to 1\. Can you see that y is going to be 0.4? Yes or no?

The Admin: So if you see we are starting with weight of 0.3 and bias of one. Right. So if you quickly add in this where is our weight saved? Wait a second. Okay. Sorry. So we have 0.3 plus bias is 0.1 and inside we have our data which is one. So into one so this is coming as 0.4 four and then we have the rail outside.

The Admin: ReLU essentially says are you positive? Okay, I'm not going to do anything with you. Are you negative? the value is zero. That's all it does, right? So 0.4 Reu is going to be 0.4. Okay, but we wanted two. So 0.4 and then we have two. So error you're going to see is 1.6. So we are off by 1.6. Similarly, if you add this equation, you're going to see we are off by 2.3. And if you check this then we are saying essentially 0.3 into 3 \+ 1 and that is going to be So this is.9.1 1 4 is what is expected. so 1 \- 4 is three. So we off by three So we have three examples three outputs. So we have 10 samples going in. We have 10 outputs. Right?

### 00:45:00

The Admin: And you can see now we have output and the loss being calculated for every single sample. So I need to average it and that is where this averaging is coming in. Right? So this is one negative 1.6 square. This is There are loss, cross entropy loss, binary entropy loss, KL division loss, many different kind of losses. We only looking at a simple MSE So divide by three. Finally I get my loss as 6 5617\. Now I need to calculate the Gradient of the only weight I have in the equation. So I essentially need to calculate delta L by delta W. Okay, this should be easy. So if you look at this guy is positive so not required. this is actually X and then B if I don't want then it's actually X right?

The Admin: That's why the gradient is going to be I think R also taken somewhere over here. So we have this one clear on this. So every single step we essentially updated. So now we have updated W1 and bias has changed. data blue is changing and slowly you can see on the bottom our loss curve is dropping right the learning rate happens to be 0.08

The Admin: 08 and as I said we have this negative always in front that's all you need to know this is something we covered in session one so just a recap of what we did there right and I'll just did a run and see how close can we go we have hit an error of zero already right so a simple equation so simple in a simple manner we can solve it okay there's another widget now we have w1 same And this is a slope that we have. And then this line is what we are also changing. So in the run one we have weight three output is 24 and 16 is what is expected. I think I wrote some text or explanation of this also. So this network turns the input 2 into 24 and we want 20\. Right. That's a simple equation we wanted to solve. Two loss.

The Admin: 16\. How do we know that? Can anyone tell me how the loss is 16? Can you see the vision and tell me?

Keshava Murali: Because it's square of four 24 \- 20 square of it mean square loss.

The Admin: We are talking about the square loss, So 24 \- 20 comes to 16\. So now as we change the weight, you're going to see that somewhere over here is what we want, right? So if you increase the W, what do you see loss? I just want you to focus on this table. If I'm in what is happening to the loss? Increasing. Right?

chirag Tagadiya: Increasing.

The Admin: And if I reduce the weight, what happens? It is reducing. But if I reduce it further, what happens? it is again increasing. This is the point that we want to find where the loss is zero or close to zero. the loss will never be zero for every single weight. We need most of the right weights to go to zero unless we are okay to because it's impossible to satisfy everyone right if you are running a family then you can't keep everyone happy so you need to figure out who you want to keep happy there is one weight that not wait I should not call one light weight that you should always keep happy and everyone else is okay all right now let's follow the backward path how

The Admin: How do we actually do it? Okay, and this looks complicated, but it's going to be very simple. So, we have X coming in. The equation is W1 into H. And that becomes H here, right? We may add some activation function on top of it. Let's say ROU Swiss or GU or ALOU or PO or all of these are there or All of these exist, Or what is leaky, right? If you have a kid, you order leaky. Now that H might get multiplied with one more weight and becomes W and then becomes Y.

### 00:50:00

The Admin: So the loss is y minus t whole square right the reason we take square and even if we do not take square we want to go with l1 that is an absolute l1 right we do not so we basically do not take the negative and positive from there negative positive we take from the equation from the graph is going down or up right that's why square always gives positive numbers that is interesting for us another benefit of square is and I wrote a blog about it but I don't know where the link is okay it's not harsh We want f and This is sometimes I feel I shouldly spend at least 5 six days just on mathematics not to teach you math but to teach you the beautiful side of math right let us say we have 0.9 minus 0.81 what is this equal to 0.09

The Admin: 09 of course. But now if you take a square of it, what does it become? Anyone right?

chirag Tagadiya: 0.081

The Admin: So this is the absolute loss and this is the L2 loss. You see that we are slightly okay here. You're being a parent whose son or daughter gets 81 out of 100 and you're saying it's okay. You're not Sharma Gi. This is very absolute saying that look at Sharma Gi that his son got his daughter got. So the question is that how much you want to penalize and it works in a reverse way also by the way. because if these values were bigger the square is going to be massive because if the numbers right so if anything is between 0.0 99999 we take a square of it becomes smaller only. So that's where the square comes in.

The Admin: But if the number was any bigger then this is going to be super critical that I don't like what you're doing in life. You will go in that mode. But this is the equation we have. I wanted to look at h which is into X. Then Y mentioned here as W2 into H. And then we have this thing and then we have a loss. how many of you remember your 12th class mathematics? this was taught in 11th. When did you learn differentiation? Can you do a differentiation for this? So right now we have this L is equ= to Y \- T².

The Admin: So if I say D L and then we do del Y this is going to be what 2 \* dy important.

Manjith Adapa: One minute.

sonu agarwal: Wait a minute.

sourav dhar: is what?

Vaibhav Lohar: Okay, bye.

Vaibhav Lohar: Thank you.

The Admin: So this is the equation we have. That is what the equation you see here. D L by D Y. Can you see that same equation? Next we have D L Can we do del Y by del Y is H. So can you do for that? So Y is into H. by delh is equals to simple w2 into by d y I'm not writing it.

sonu agarwal: How you doing?

The Admin: So this is equals to what? Simple w2. Correct? Yes or no? Okay.

The Admin: And similarly if you do for here del L by delh you're going to get one right. So you can see that the same equations we are driving here. So that is how we calculate the weight of every single one. So if this is the model this is where the input comes in and this is where the output goes out. We calculate the loss here and then for each weight we start calculating the dl by dw and that allows us to calculate the d by dw for the weights before them and that allows to calculate d by dw for the weights before them and so on and so on and this task is done by autograd autograd is something that has allowed people to and this is mathematical right it's a pure deterministic calculations so this is how we calculate by del w2

The Admin: Del L by DW1 and calculate the rate of change of loss with respect to weight for everything in the new network. The same 64 number is coming here. So we have d by d y which comes at 24 \- 2\. So remember that l 24 \- 20 into 2 8 we now have d l by d y. you take it to next calculate d by d2. Right? So the whole chain essentially follows one step at a time. Clear? And of course if we change this all values are going to change.

### 00:55:00

The Admin: So what is out autograd doing is autograd is looking at and this is why by the way where pytor was pytor one over tensorflow today we don't even ask but every time I will start a course people will say why not tensorflow and the reason was tensorflow autorad vers python autograds were really good in tensorflow you had to be either so most of you don't even know about this have you heard of cafe of course you have heard of cafe Yeah,…

chirag Tagadiya: Yeah, I think that's some framework text neuronet number.

The Admin: I do not know when I did bookmark this but I wish there was a bookmark history also. I would have bookmarked this in 2015 I believe. Right. So we used to have something called cafe. This is the one that we used to have to be able to train a neural network. Right. And this was doing autograph at that time. No fancy stuff. from there densiflow came in really good but pytors when it came autograd was killer. They did a really good job in writing the autograd which calculated the back propagation for So This is the whole code that we are going to be interested

The Admin: So model some architecture we're going to discuss and head weights everything is designed there the kind of attention layer we have do we have chronic embedding or not everything is moral that is separate this is reality this is the reality of our life this is how much money we can spend this is what is left after everything paying taxes and E20 fuel and EMI and everything. So this number you should look deep into this number and realize where do you stand in your life because this number is big then you're doing really good right?

The Admin: So we have a model that can be anything model like model we can decide to actually make a one trillion parameter. we make a one trillion parameter model? We can make a 100 trillion parameter model. Making is what just a Python function but we able to send a batch to it and on a GPU is going to be the reflection for us. So we need to come back to ground at that time. So we take a batch decide what the batch is and how big it is really depends on the money that we have. Then we get the logistics out. It goes inside the GPU, calculates the things and Then we send it to loss function. It's saying America but we want Canada for example. Right? Those are the things that are being compared here. That gives us loss. Moment we back prop all the gradients are saved in the memory. We have not updated the gradients. We have not updated the weights yet. Are we clear?

The Admin: Till this particular step we have not updated the weights. We have calculated the gradient. So we have the weight now and then we have the deltas also. But the addition or subtraction has Not yet. Are we Very important. Yes or two things are happening after this line. Right now you do not see any update as now. Of course you're not seeing any gradient accumulation. If we say that we have gradient accumulation of 100 then we're going to put this box in a separate loop that runs 100 times and then we are going to run this one times.

The Admin: Can you imagine that happening that we have for i= 1 to 100 and that is happening 100 times and then once that loop is done then we take this one that is all a great inclination let's say that's all we have to do clear what is great inclination do your back prop 100 times and then let the optimizer step happen once Yeah, I don't XF \+ 1 B.

Anirudh narla: So this is what you meant by XF \+ 1 B right. the

### 01:00:00

The Admin: Yes, F \+ 1 B. Correct. This X is okay, Nathan. Hello.

NITIN YADAV: So there is one doubt I know that is right but I just want to be your so let us suppose we are updating the weights after accumulating the gradients.

NITIN YADAV: So does that mean that it is what it's supposed to be learned in the second step when we are updating the weight.

The Admin: No, no,…

The Admin: no. Hold on. Don't even think like that. What is happening is I asked you to get me 10 kg of ata.

NITIN YADAV: Okay. Mhm.

The Admin: You can go and get me 10 kg of ata at once. But your leg is not good.

The Admin: your leg is hurting so you decide to get me 1 kilogram of ata 10 times that's all that is happening so instead of doing those parallel things we sequential had I had more money I would have bought thousand GPUs and not wait for 100 steps but because I have 10 I have to save the updates 100 times and then update once mathematically they're exactly same mathematical change at all right instead of so in okay so let's say

NITIN YADAV: Okay. Yeah. Yep.

The Admin: Let's say we had 10 GPUs but I have one. So my gradient acclimation step is how many gradient acclimations I have? Not 1000 because I can't write 100 values. Is this part clear? tell me 7 \+ 8 \+ 9 \+ 10\. What is the sum of this? Anyone? Can you do it quickly? Do you remember equation for this?

Vaibhav Lohar: 55

The Admin: This is 55\. Yes or no? So, this is what gives a 10 GPU system does this. \+ 3 \+ 4 \= 7\. Fourth step 7 \+ what do you have now? 5 \= to 12\.

NITIN YADAV: Okay. Yeah.

The Admin: Fifth step 12 \+ 6 and so Is it clear now? So eventually at this 10 step this will also reach 55 clear. So I think we are adding it.

Swati Bansal: So when we are doing reading accumulation are we not increasing the memory required for the same because okay okay got it…

The Admin: That is the reason we are adding How many registers do I need? Always one.

Swati Bansal: because it's still always updating the Okay and…

The Admin: Okay, this used to when I said B there you are right 100 B's are there I meant to say updates so one step I should write it again is equals to X forward plus X backward as you said plus one update this update is what

Swati Bansal: one sorry one more question because somebody said the X is 100 because of the accumulation that X also applies to backward, So, it's 100 F and 100 Not one B. Okay. Okay. Which is…

Swati Bansal: which is optimizer. Okay.

The Admin: which is the optimizer.

The Admin: Okay, he used to my favorite question when there was a time I used to teach Python. can you believe there was a time when people used to pay money to learn Python? That is the right question. Okay, I have x \= to 4 and then y \= to Python is so old now that I have forgotten the question also. So imagine that y is equals to 4 and I want to add let's say three to it. How many memory addresses do you think we need in Python?

The Admin: So if you think from memory perspective and this is important for you to remember in Python everything that you read x= to 3 and everything what is This is actually a pointer to a memory address where four is stored. So when you say y is equals to 4 it is pointing to a particular memory address where four is stored. So when you say y is \= to 40\. So okay we say let's say y equal to 4 in python. Press enter.

The Admin: Then we say y equ= to 40\. What do you think will happen? Anyone else?

chirag Tagadiya: Address will change.

The Admin: Two scenarios.

Anirudh narla: points to a different object.

The Admin: So either this will happen or this will happen. Y is going to be This is the whole logic. behind Python or what exactly Python is and how is it different from C and C++ this is what happens you say that now that address is actually a integer or is going to save a bigger address whereas in Python we always reference by address so here we are actually going to when you say y is equal to 40 now suddenly the kernel has to figure out to a memory bank or memory area where it needs to store 40 and y needs to point there four is still there if someone is pointing to four four will be there otherwise

### 01:05:00

The Admin: the GPU is going to take care of that and…

chirag Tagadiya: Garbage collector will collect it.

The Admin: remove that. So if I ask you now let's say y is equals to 4 and then we need to add one to How many memory addresses do we need in Python.

NITIN YADAV: Three.

The Admin: Of course, right? We have to store four somewhere. Four is stored. Then we have one. We have four. We are saying y is equals to four. And then all we want to do is equals to y \+ one. So we have four. Then we have to store one somewhere. And whatever value we get here that is going to be five.

The Admin: that we have three memory addresses that required. Are we clear on this? Okay, that is exactly what is not done On the GPU side, when you say you want to add one, one will be added here from some other memory bank. So, one will be saved in a temporary memory bank, it will come here. All is not required. So, one directly becomes five fast. You do not need more memory. That is how GPUs tend to work. That is autograd that's why everything at the back end is C C++. Are we clear? If you were to write this in Python, then open will not be there and we still have hope. All because of C++ we are now in this particular other important thing. So we learned that till here we have not updated and the moment we do optimizer step we update it. If you are seeing graded incrementation steps then we may do it 100 times and then only call this once. Also this is called optimizer.

The Admin: step and optimizer we learned we have relu we have gaoo we have su and many different optimizers exist now we have not discussed optimizers yet we are going to discuss optimizers but there's this beautiful optimizer which is called Adam right we have this optimizer now we have something called sgd stands for stoastic gradient descent it is used for CNN's and it is not used for fully connected layers or it is not used for linear layers right it does a gradient information at once so you may never you may never learn about SGD in future but you need to know that it exists then we have something called Adam now imagine that we have a weight one and then we have weight two and then we have weight three I'm talking about but let's say weight one was associated with a token t1

The Admin: T 100 and T1K. Weight 2 was largely associated with changing T2 and T200 and T3. And weight three was changing token number T4 and T19 and T6990 something like that. these are the words So we have the and so on. And these are words like a and about and something like that. And this is the word for photomorphism.

The Admin: Then T19 stands for accelerating and D990 stands for boot sequence. how many times do you think our data set will see this versus this?

chirag Tagadiya: Photomorphism will be there.

The Admin: This is rare, right? Yes.

Manjith Adapa: Yes.

The Admin: No. And this is very very often,…

Ritambhra Korpal: Nice.

The Admin: And this is also very often. bias was unbiased. SGD would say I do not care about how many times the weight is the concept wasn't there actually. So SGD will just calculate the gradient whatever comes in it will just update the weight. Then Adam came and before Adam we had something called RMS prop. So Adam is a child of RS prop team but same concept. So Adam came in, Adam said that as I'm recording all of this, I'm seeing that there are some parameters that are never updated because the tokens the data that required is very rare for that. So it came up with a very different philosophy. Adam says that weights that are updated more often, I will have a low LR value for that and weights that are updated rarely, I'll have a very large LR for that. LR LR this is low and this is high.

### 01:10:00

The Admin: So Adam is an optimizer that tracks every single parameter and records in the history how many times I've been updating this guy and with what kind of greatness I've been updating this guy because I do not want to miss an opportunity where I get something special clear on this Adam is what made these deep networks possible especially on the linear layer right where we have these LLMs and the stuff okay I just want you to see the history of these things because we have RMS prop and let's go to Vicki and ask who made RMS prop. Jeffrey Hinton. Who is Jeffrey Hinton?

chirag Tagadiya: the Godfather. It's

The Admin: …

Rahul Uniyal: All the fruit.

The Admin: and he just made it in some course that he was teaching right and it's not 6 months ago it's years ago but it has some issues and after that the idea came in then someone improved and made Adam but the real credit goes to RMS prop and after that we have Adam which is now used by everyone so Adam is something. that essentially takes care of which weight should be updated, how often and with what kind of value. So we have for different weight I'm saying wait weight do you understand the difference in weight as in hold and…

Ritambhra Korpal: What?

The Admin: the other is weight which is weight we discussed some weight here which was8 somewhere yeah you see this 0.001 01 or here at least you see this negative now if I step you don't see that changing right so and there LR was fixed over here on me where am I looking for it this is 4 you see that…

Ritambhra Korpal: Yes.

The Admin: how many weights am I mentioning here one I have one parameter so I can't even show it to But if I go probably on the first one here we have two. Thank you. here we have two and here also we have one is not shown here. But You get the point right? till now we have discussed only one LR for the whole network. But the moment Adam comes in it's going to save the weight or save the LR for every single parameter. It is a blessing in disguise.

The Admin: This guy allows us to train. But this guy also causes one big huge problem. What is the problem?

chirag Tagadiya: Money.

The Admin: Earlier 1 billion parameters and that needs to be in the RAM. Now I have Adam. And we're going to see how much Adam costs us. And then we need a lot of RAM for Adam. You do not take Adam, you can't train the guy. but if you take the Adam, then you need money. And life goes on. So that is what Adam is and the reason we were discussing Adam is because when you see that zer which optimizer is taking that step happens here. Are we clear?

The Admin: This optimizer step essentially means that it's a Adam step or is a SGD step or because optimizer has to update right finally optimizer knows that okay I don't want to save all the history I'm just going to update with currently what I have edged simple cheap no cost Adam very expensive and by the way this is a very interesting time to introduce you to something called Adam versus I forgot the name Chinese are using it anyone Leo something like Leo only.

Smita Sasindran: Me on.

The Admin: And this is where the fight is happening right now. because Leon takes a very very low amount of RAM compared to Adam. I'm hoping let's see and these are the decision that we have to figure out. We it's not Leon something else. Okay, we'll talk about it when we talk optimizers. So now we are forward, we have a loss, then we add them and then we have to update, right?

### 01:15:00

The Admin: So that is where this item comes from. So slowly our loss is going to come go change and weights are changing and this is something that we'll see. Okay, this is already I'm so happy. Same explained in a batch. No problem. would you believe that if I tell you that gradient exclamation had error till 2024 every single gradient exclamation in every single pytor kas tensorflow cafe everything had a simple error and people didn't know because the error was such that you can't find it easily then somebody actually figured out that there's a big error so even the charge GPT the GPD 3 3.5 were train on this error the error is if I have microbatch one microbash 2 and microbash

The Admin: And I have the average loss of 2 2 and minus 5 there. The correct combination is going to be The valid tokens that I have then four into two here and then two tokens into five. Remember the last session where we are saying that if you have pad tokens we're not going to calculate loss on it. Remember that sometimes we have to add tokens when we are training on As there definitely loss on tokens is going to be to less than the total number of tokens in example. Yes or no? Right? Especially in the post training, we ask a question and they answer we do not calculate the loss on the question. That is exactly where the error was that if you were using gradient information, then you would be actually just averaging the losses instead of multiplying with the token. Delta difference is very small. So people didn't realize but still it's a waste of money. Okay. Now comes the important interesting part.

The Admin: This is one more domain where you guys can think of writing some research paper of your own and if you're interested go deeper in this particular field. the question is how does a computer actually store a number? What is happening inside a GPUs? we discussed that we have brain float BF FP8 int8 and lot of different things that is just a format of how do we want to store the number finally in the memory. every single ite description of let's say B 6 FP32 or FP18 16 and other values has three things inside it. The first digit mentions the

The Admin: Whether this number is positive or negative then we have something called exponent and then we have something called mantisa. Now I wanted to understand this because it will quickly help you understand for which weight or which kind of parameter what kind of data type we should have or you should have. So look at FP32 we have 32 bit The first bit is sign. After that we have eight bits of exponent. Then we have 23 bits of mantisa. Simplest way of understanding this is me writing a number. So I'm going to write a number and I'm going to write a number in a bleeding red because all of you sleeping. So I'm writing a number here. Can you see the number?

chirag Tagadiya: No.

Manjith Adapa: 123.13. Yes.

The Admin: I will not return it.

The Admin: If I write a dot here, what is the number? Okay, you see the difference how easy it is to convert something into a decimal number. Or I could have done this also. So you're seeing You're seeing what the number actually is. Mantisa and exponent how big that number is. Can you separate those things those two things out from your head? Right?

The Admin: what the number actually is and how big that particular number is because I can make it very small just by multiplying just by doing 10^ minus3 or 10^ \-4 this is coming from the exponent and the detail is coming from the mantisa clear on this okay second thing is I do not know off my head so do not quote me anywhere we have floating point 32 FP32 and then we have FP64 FP6

### 01:20:00

The Admin: 64 looks like a bigger number compared to FP32 it is but when you're talking floating point so what do you think the difference in these two would be forget about a mantis and exponent that we're discussing one difference that should come in your mind is that the FP62 is way more detailed compared to 32 right it is way more precise what do you mean by way more precise what I mean is maybe and I'm going to be not writing infinite numbers here so apologies because I'm not mathematically correct But I'm conceptually correct here. Let's say I can write 0.01 1 in FP32, right? But

The Admin: After that I cannot guarantee a 1 2 3 4 all the numbers after that I can guarantee only a five. Right? So I can do this or I can do this or I can do this. Are we clear? This is the precision part. After how many digits am I precise? If I had FP64 I would be able to do and then I will be stuck at zero and zero here. Are we clear?

Manjith Adapa: Yes.

The Admin: So that's the difference F32 and 64\. So one thing that you need to know it is impossible to come up with a system that can save every single number humanity can represent.

The Admin: You cannot write all the numbers on a computer because you have something like this building inside right first thing. So whenever we write a banking application super important deep scientific calculations you need to be aware of what floating point you're using or what numbers you're using because you may just not be able to represent them. Second is u as we go deeper we need more RAM to be saved and as we go this side we lose the accuracy or we lose the detail basically we have. So, this thing I'm going to be calling resolution. Are we okay with it? I understand resolution better. I know that 720p, 320p, and you can still see the video, I can still send you a 320p video versus a 4K video and you can still see the damn thing. But the resolution is How fine can we go is changing, right? So, I'm going to be calling this thing a resolution. Are we clear? And this depth we are going to be calling the scale of how small the number is. Can I represent 50 zeros and something?

The Admin: I can't even represent four zeros and something. So that we are going to be calling this a scale. So This come from a bigger mantisa and this comes from exponents and…

Anirudh narla: These are different quant right at the end of the day a quantization of a LLM basically with less numbers.

The Admin: I do not know what is I know These are data types. irre irrelevant question concept right now do not think.

Anirudh narla: Okay.

The Admin: Okay, now we have a table here and we will not spend a lot of time but I still want you to understand this.

The Admin: So whenever you do get time try and see what is happening here right I've tried to make this because I did not find this kind of calculation anywhere okay so walk with me because it will be messy so I do not want to be lost and have a yellow color selected of all colors which color should You see this is the problem in choice. You give people choice and then they get confused. Let me pick this. Red only because red will hurt your eyes. So we are discussing FP32 first. Here we want to store a value of 0.1. You can store other values also. If you click it will change. Then the first bit is going to store the sign bit. That is zero here. 0 is positive, one is negative. Fair enough.

The Admin: Then we have mantisa. So we have 1 2 3 4 5 6 7 8\. How many mantisa bits we have? We have eight bits. why it works like that? Do not even ask. The way it works is we just say 011 1 0 0 1 0 1\. And if your 910 class, then you can calculate that number represents 123\. But we do the maximum of what this number can represent and subtract it from there. The maximum we can write is 127 till here by the way. Right? and first let me show you that if this was zero that number is Look at this 127 and look at this \-4. Right? I want to keep looking at that.

### 01:25:00

The Admin: So if I change that number that is changing are we clear? If everything is zero then we are saying 10^ \-27 we are saying 10 \- 122 we are saying 10^ \- 106 we are saying 10^ 22 are we clear on this I want to be super clear on this that is how we calculate what is that 10 to power something that's how the mantisa gets involved hands up or hands down

The Admin: Okay, thank you. And finally, we have the bits here, So, you wanted to represent 0.1. How do we represent 0.1? It's very very difficult. And you can see how many bits are required. And even after those bits, we still do not get 0.001. So, you got this 48 by the Same 48 that we have here. The scale right now is 2 to 48\. So, we are going to get this huge number 28 47 498 and then 1 2 3 5 6 7 8 9 zeros.

The Admin: The mandis are bit the ones that are below we have 1 0 0 1 1 0 0 1 1 0 0 1 1 0 0 1 1 0 0 1 1 0 if this was 64 we'll have 1 0 0 1 1 0 0 continuing there from the first one you're going to take half then 1x 4 this is basically 1 / 2^ 1 2 3 if you remember 9 10 then this is easier and when you add all of that you're going to see that we're getting something like 0 six once you add these things right then we have A free leading one a concept in these things where the freeing one is added.

The Admin: So we multiply 1.6 into that huge number that we had that we get got from Mantisa 28 something. It became this huge number. What am I missing? And finally when you read it back it's going to be read back as 5e 064\. I'm missing something here. I think I changed something I changed those digits and I'm calculating sorry yes so I change the mant that's why the big change so right now we're getting 10^ \-4 uh \-4 sorry so 2 \-4 gets us to 0.06250 0 then we added all the minus that is 6 correct we add 1 to it which comes 1.6

The Admin: six and then finally we have this into this number and finally we have one that is made here. Are we clear? That is how we actually calculate all of that is happening in the GPU at the back end. We do not have to worry about it. We have to worry about what is stored in these numbers. Right now as you change these numbers you're going to see that digits are lost. Any question? Yes or no? Okay, this is FP32. let's go to FP16 and see what changes. Both have changed. Do you see the mantisa and the changing? Exponent is orange one and up. It's down. So it has low resolution and it has less capacity of representing the big number small number also. Right? Both have dropped here. But look how smart Bflat is.

The Admin: Believe this B float is invented by Google deep mind. The same guy who got the Nobel Prize in chemistry interestingly right Dennis Hzavaris. So this guy and look at B float exact same exponents reduced mantisar very interesting and these are different formats that you can explore later on but I want to focus on B F16 and BP FP32 okay and we will quickly draw it to understand what is happening in these two cases. in FP 32 let us say I can represent 0.000000

The Admin: 0 0 0 0 lot of zeros and 0 1 2 3 4 5 6 and after this that five 0 shuffle starts right but here I can represent everything so I can represent 6 5 4 3 2 1 and I can represent 6 7 8 9 10 this is my problem I can't do after this here in FP 16 what will happen is 0 0 I can't even reach that far. So here my shuffling starts becoming zero on this side. So I cannot present these numbers. Yes. Understand difference between FP32 and FP16. I do not have that kind of precision. my exponent is also not big enough for me to represent that small number. Now we have brain float B. This is B float. This is my dyslexia hitting exactly this moment. the B float 13\.

### 01:30:00

The Admin: What it does is it allows me to do go all the way and somewhere over here only sometimes it will let me pass until here I can actually represent numbers right but sometimes 55001 so this is exactly what I meant by 4K versus 360p so I can represent those small I can go that far but my precision is not high right I'm

The Admin: I heavily quantize that particular part. I'm heavily alienate or heavily pixelated that particular part but I can represent that number. I will be off but I can go there. Are we clear? I can represent small numbers but my resolution is low. So possibly I can say 0.0015. Right? This is what Bflat allows us to do. FP16 stops here. So it doesn't go there. FP32 would have let me done 1 2 3 4 5 6 7 8 here. Are we clear? So FP32 lets me do 0.0 very long distance 0 1 2 3 4 FP6 000000 stops here. It does not even let me represent small number. Then we have brain 416\. Lets me do 0 0 0\.

The Admin: But my 1 2 3 Good way to understand 1 2 3 4\. I'm just focusing on this 1 2 3 4, right? It will let me do 1 2 3 4 or 1 3 4 3 or 1 1456 or 1297 or 14 or 105 and so on. So it lets me go to that number but I lose precision earlier right FP32 would have allowed me to do a much bigger precision. So my chunks are bigger in case of brain float but it does allow me to go there.

The Admin: The benefit of that is as we start training and this is what is explained here the smallest number the FP13 can store compared to B brain float is same right I can go to \- 38 FP3 I can't even store 10 to minus 5 right because has dropped my exponent is same as the FP32 my ment is small so my chunk size is much bigger Why this is important is because as we start training as we are at the end of the training or initially also if my gradients are small which are very very small we have a big learning rate also in FB 16 if the gradient is 10 \-4 okay but if the gradients are 10 \- 6 I start losing and if I become 10 \- 8 I can't even store it there right green float is really good in all these three that is one big thing because it gives a higher

The Admin: accuracy and I can store two BF in one FP32 that's the only reason we're discussing it right so in FP32 I can store two of FP16 or two of BF16 32 16 into two right so I can store double the data we clear that's why BF16 is much better compared to FP16 if you can use it properly So FP32 goes to a very small number. If your gradients are becoming bigger then you see that in FP16 you start losing those numbers after this particular point and if the loss scale is if your loss sitting some over there then we are gone.

The Admin: If you are somewhere over here then it's still okay but we can't guarantee we don't know where our loss is going to sit right we don't know where the gradients are going to be some and we are using Adam which means some gradients are going to be small some gradients are going to be very big so it's very safe to use FP16 it's not safe to use FP16 BF16 is much much better any question on No. Why did I say that you can write a paper on this? Go back to the same big boring widget. I made something for you.

The Admin: Custom make you can decide how many of exponents you want and how many of mantisa you want and for some applications you can come up especially if you're in FPGA or in chip design may not be or if you do enter believe me in 3 years we can order a custom chip you can do it today but it's going to be so easy that you can design your own custom chip and in fact I don't know have you seen this PGA A LM. So this is a Chinese team that has made $150 FPGA system motherboard which can $150 literally 15,000 rupees today 14,000 something which can now run B full Q4 only sorry

### 01:35:00

The Admin: But This is dropping tremendously. So if someone else further optimizes this then this is going to be easier and FPJ is we essentially writing a computer inside right but you can make a custom system also if you were to use FPGA. in that case you can actually come up with after training a model you can come up with your own schema of things by looking at the weights that my precision is here these are the small numbers I have then you can actually come accelerate it faster right so if you ever think about these numbers I don't know why will you be sitting alone and thinking about should I invent a new e data point or d type but just in case sometimes happens right you're fighting and maybe with your wife or your husband and he or she

The Admin: screaming or your child is screaming the hell out of you, then you certainly go inside a thought. What if I were to implement it data floating point number? If that thing ever happens, then this is a custom widget for you. Nvidia came up with a lot of interesting things. We have FP8 also, right? We are pushing this down to the hell. We have FP8 also. This FP84 M3 works. Then we have this. And we are going to be using FP8 by the way. FP8. and Nvidia has done a tremendous amount of work there, Using FP8 and FP4 also in transform engine, And for this we needed a Blackwell series that we didn't have last time. So we couldn't use it. But this time we going to be using Blackwell. So we'll have access to all of that. So FP8 gives us even better performance, right? We can go as small.

The Admin: And you can see that the numbers I can represent here are very weird. So how do we actually manage that? We have a recession for that FP8. You can see that I have a 1.56% error for one. But if I change it to 1.3 then my error increases for 001 I have a 100% error there. So we have to be careful of how do we handle such things. I can't even represent that. So I have a range in which I can represent. So if I scale off all of my number outside the neural network, I can handle this. Can you think about that? All I'm saying has error of 2.3%. 01 has a 6 95%. 01 100%. So what if I store the divide by,000 outside thinking in that direction that allows us to do magical things. That's what Nvida did and acceleration is insane.

The Admin: So if we check FP8 versus F4 training and if you go to images throughut yes you can hit double the training speed right we have 44% MFU we about to discuss but 67 % of MFU. If we allow me to be a bit of racial if you were all in US and we all were negroes and then we say MFU then you might get wrong thoughts. Okay. So we discussed this. Yes.

The Admin: So these are smallest digital digit numbers we can represent but we will come back to it on how do we handle this new format not in today's session I kept it here so you can come back to it some concepts we are going to discuss then is that we are going to figure out what the outliers are for us there are some numbers we don't want to represent we know that they are not good fun we're just going to throw them away and we'll talk about how many numbers do we have each block we're talking about that our new network will only be trained on these 32 numbers I'm network train only on these four numbers because that's how you keep hearing bit one have you heard of two bit new network Microsoft keeps coming up with these concepts 1.3 bit neural networks 1.8

### 01:40:00

The Admin: 8 bit new networks that is what is happening here the whole neural network is just built on these 32 numbers right so we will discuss how this happens but conceptually I've just kept it here guarding a needs one batch yes there's a concept called gradient null and then gradient clipping now when we train our models sometimes we have a very bad example that comes in that tries to just let's say we just added a lot of sanskrit right that happened to us we are training Hindi Sanskrit and Hindi

The Admin: If you were to write some logic to identify Hindi versus Sanskrit, both will be classified as ones because the same characters are used there, So, Sanskrit certainly entered and we are seeing our Hindi which is going really good. Suddenly it's like what happened the loss is off the roof. So we need to make sure that we have something that clips and we clip the gradient norm in one. We do not let a more than one gradient norm ever flow back. This is coming from the empirical studies that people have.

The Admin: If you don't then such big gradients are going to come in and you see where the greater norm comes in and where the loss starts speaking up. Can you see that? Very important. You not doing good in life today has nothing to do with what happened yesterday. It has something to do with Maybe last year. Same thing is happening here. A gradient norm that screwed us earlier is going to show the loss later on. So do not blame your friend, family, partner for yesterday. You can blame them for last not yesterday. last month you can say 10 years ago that's fine. That is completely fine. But here you can see that the norm that hits the model early is what is going to hit us later on. I care right that's why a very famous person said do not blame yesterday blame last year.

The Admin: Who said That should be here when I zoom. what a step cost us. you understand What is a step? X backward button, one gradient update.

The Admin: What does it cost us? Let's say we have a weight and we are saying that we are storing the weight in the BF16. For that we have to use two bytes. One bite is 8 bit. So B of 16 16x2 is two. 16 by 8 is two. This should be clear. Then we have to store it ient. The thing that we're acclimating or not acclimating this has to be in the memory has to store somewhere, right? Then we have a full precision copy in FP32 of what?

The Admin: of this guy. So we do all the calculation BF16 because we have to be speedy and fast and blah and blah. But we have to store a full copy of that otherwise the error accumulates. So that is also there. Then we have the optimizer the uncle Adam is going to store eight for parameter. So for one parameter that you say manual network is one parameter you're actually saying I have 16 bytes for that parameter. Are we clear? One good life, two people, their kids, their fees, your car, how am I and everything clear? Single, no Married, lot of training. There's a lot of training. Okay.

The Admin: So what that means is that if a model is two billion parameter you need by 30 GB of RAM just to store single we not even talking about the batch size and how many samples you want 20 billion parameter 298 GB 120 1.7 TV are When the model and we say that we want to save a checkpoint, this is the size of a checkpoint. This is not the model that you will share with people. If you want to resume the training of your model and this is very important for you to understand because many of you will be involved in the training process.

The Admin: When you say that we have a checkpoint of 120B because we think we have reached a particular state you're essentially saying you're going to be now saving 1.7 trillion 1.7 terra byte model because it needs to store all of these states it need to store the weight the gradient the full precision copy and the optimized state because next time when you start you want to start from the same optimizer atom states because you've been acclimating all of that right we've been training for 200 billion parameters after that we don't want to continue so each checkpoint is going to be super heavy and all that remains in the GPU which means that if now you say that I want to train for 1 million tokens then suddenly I have to see that you already have so much EMI now you're saying that you want to buy a villa in Goa right that's where we'll discuss about few things now so I think

### 01:45:00

Swati Bansal: What are those two running numbers for Adam? yeah,…

The Admin: We discussed right Adam needs to store that was this parameter updated earlier or…

The Admin: not? If it was updated what was the frequency of update and what was the last update? We just discussed how Adam is different from HDD.

Swati Bansal: you mentioned it has to store learning rate for every weight.

The Admin: So that result cannot I miss half of your words.

Swati Bansal: But there can be ways to optimize that, Because for example, does it really need to store for every weight or can it go for a range or something? Yeah.

Vardhan Walavalkar: Sorry. What is it called? I'm sorry, I missed. What is this full precision copy in LP32? What is that for?

The Admin: The calculations happen in floating 32\.

The Admin: Every calculation happens in FP32 because that is where the precision is. So when we calculating the calculation of gradients happens in FP32. and then we convert them into extra hundreds usable probably 10…

Vardhan Walavalkar: Okay.

chirag Tagadiya: How many checkpoints did you save in era v4?

The Admin: but hundreds in as yes…

chirag Tagadiya: database. Copy.

The Admin: why do you need checkpoint you need to figure out how well the training is going and for that after a few billion token training we save a model and we are also afraid our system might shut down. So after 2 hour of compute after we spend enough money basically again goes back to money how much money have we spent $100 save one…

The Admin: because if that is lost then everything is lost right…

chirag Tagadiya: Do you still have this checkpoint or…

chirag Tagadiya: you deleted it? Okay.

The Admin: that model then goes for the test and validation. So if you want to follow how your model is actually doing on test and validation you need as many checkpoints. Now is that important? We kept only last two and the last best. So if we had something better in terms of validation, we will store that and then we'll store the last two. We keep overriding it. These are huge. The amount of RAM and storage that we need is massive. this. So if your model size is big, do you see that interest rate going up? Do you see Nirmala Saramun smiling slowly at you? There's a hole.

The Admin: wide This is my smile. Anyways, watching a run that last week. How do we do that? Loss is easy to calculate. Gradient We We need to make sure that grad norm is stick to one. And then we have tokens per second. That is what is telling us how many tokens are we processing per second. And then we have What is MFU is model flops utilization. this ask what percentage of the machine is are we generally using a forward and backward pass costs roughly six n operations. N is the number of parameters we have right so if we have n weights 1 billion parameters then 6 billion parameter is a very rough calculation of the total number into tokens per second that we're calculating.

The Admin: What this means is if we have 10 billion parameters into six is the number of floating point operations into let's say 10,000 is our let's say 4k 4096 we are right now doing 247 floating points per second that is what is required are we clear but this is what we're consuming per second divide by what the machine can do much faster here is a number which You will see and you'll be surprised what we achieved for a 9 billion parameter at 12,000 tokens per second on H 100 is 6848 teraflops. The actual capacity of the machine was 7,912 teraflops. So our MFU was only 8.2%. You might think It is a small number compared to what is Potentially possible is something like 35 to 50\. If you hit 35, we are doing tremendously good.

The Admin: What brought this number is RAM right now that number can be 35 if we are not using mixture of expert We were using If you don't use mixture of experts then I need to have massive RAM because I can't optimize that right? My RAM goes up. So the option is to go for If you go to experts RAM drops but the network the MFU or the overall utilization of the GPU drops. So it's a slower thing. Second thing is we did something called reversibility. It is there in the lightning link that I shared earlier with Reversibility allows me to squeeze best out of the RAM side. We were RAM constraint. We were not the compute constraint. So that's why we agreed for that kind of performance. You can see In fact at some reason six times worse also compared to what is possible but we were at least 10 times better in the RAM. Right?

### 01:50:00

The Admin: So if we don't do this then the budget would be we need hundreds or 200 GPUs at same time just to train what we were training on single 8 GB cluster. So that is again a number that we have to figure out what is going to be RMF. Same thing shown here in increase the model size it's better but this is just conceptual we might think that we might be able to fit something in the GPU but there's a limit to what we can do but we have to calculate MFU that is going to tell us exactly how good we are now the failures that are going to haunt us silent checkpoint misload you see the checkpoint you're trying to load it will happen for reasons you don't even know some library doesn't match the last checkpoint was saved

The Admin: using some FLA is a flash attention library that is 4.2. we started your system now for some reason is 4.1 that is cash flush divergent at scale. this would be flush not even touch upon you. Okay, this is worthy of being a paper itself. we pushed the model very hard.

The Admin: when we were doing 120 billion parameter model we tried to see which linear layers are actually learning right we are at a very deep learning stage we trained one we trained two then we trained nine then we trained bigger one right so that's a sequence we have 1 5 9 and 120 so by 9 we have consumed 200 billion tokens right so the model is really very good and after that we converted that into 120B model and we're training a 120B model so what we did we did an analysis of which layers are actually getting trained

The Admin: So if you can do that part, why can't we just train those layers only which are actually getting trained? Or if some layers do need which parameters inside need training? So we calculate all of that. Right? So we came up with a scheme where we can just train the layers that you want to train or train the parameter that are not up to the optimal and then continue. So we came up with a very similar concept which is a gradient accumation. We're going to accumulate the gradients and we are going to flush them back into the model. Right? So that worked.

The Admin: We proved that it works at in fact 9 billion scale but the thing failed in 120 and we probably wasted around four five days of B200 is a lot of money right but it did work till 9 we done that then we would have hit a speed of 24,000 tokens per second right but we couldn't so something and we didn't have enough time to figure out what failed again one paper opportunity there now clone family collapse how do we scale we're going to learn this eventually

The Admin: you're not going to train one massive model once that's a waste of time and compute and chinchilla also says you don't do it nobody does that in the world everyone starts with a small model see how it's going scale it up and scale it up and scale it up right so that's the same thing we're going to follow so can we just copy experts to make them bigger so we also need to figure out that part second is when we say that in fact look at this guy deep seek what's the model that name deep seek for before right slash

The Admin: Yes, you see this deep V4 flash 284 billion parameters 13 billion activated. So what it means is that there are a lot of experts under mix experts inside the V4 flash model not all of them are activated only few are working if you are working the same problem comes in. If you're working and then if you're not working then the one that are not working will they ever be work will they ever work who's going to make them work and so on right so it's possible that you can decide that I have thousand experts in my model but the router which decides which experts should be called doesn't focus on all of them and then the ones that are never used just die if the moment they die they cannot live again it's a very interesting thing we're going to see in the live training we'll have experts and we have to keep them busy somehow right that's

The Admin: The data shuffling it becomes very important because some experts are getting expertise in quantum physics and you are sending Gita or you're sending politics or you're sending some emoji how to design emoji or design some how to make let's say imi right in that case the quantum expert is just waiting waiting and dies right so that can happen then we have role blind expansion

### 01:55:00

The Admin: There are actually heads that can expand beyond that can be expanded like experts right we have not discussed this but once we discuss the heads this is again a problem can we expand heads and make them behave like experts because if we do that then we have a large RAM saving right so there a lot of stuff the data guarantee was never actually measured spectral upycling how do we make a smaller model bigger in that case can we make it accurate enough how do we do tests a lot of things

The Admin: that these are very specific to failures. So you need to know what happened in V4 exactly but there are ways that the model will fail. So You have to decide is BF16 is already safe. FP18 is proven. We have not trained it in V4. So that is one single drop down for us. Should we train directly on the FP8? Because we do that there's a massive improvement we get. NV FP4 is faster but needs Blackwell and we can go with all Blackwell this time. Last time we couldn't but this time we can go all blackwell so that's a good thing. So we need to take a call should we directly train on NVFP4 blackwell Nvidia has a lot of papers on that and Neotron has a library that already supports that. So if we do that we can do a short run and see how good we are. What is the clip threshold? Normally it's going to be one but we still need to figure out that do we need to be aware of NVF4. everything changes right? Are you non-vegetarian? Answer is Okay you go to a temple and they ask you are you a non-vearian you're going to say vegetarian right?

The Admin: Or you may say I'm vegetarian. I take you to a giant temple where then you're going to be completely vegetarian. So the same person can behave differently. same model will behave Same clip threshold will behave differently for FP8, NVF4 and all of the numbers. What F MFU are we going to accept? This is a compromise that we have to accept. Are we going to be going for the biggest possible reduction in RAM or the highest MFU? Both of them trade for each other, right? we trade RAM for speed essentially. That is the logic here. So what is going to be our compromise number and activation checkpoint everywhere in there are some layers. So where are we going to be checkpointing? We can do activation checkpointing also. So again a concept we're not touched upon. What is an assignment? of course I know your assignment is going to be done by applaud. So just copy paste this to claude and you're going to paste that to assignment and I'll check. We don't need to discuss assignment.

The Admin: But if you were to do assignment on your own then take a small model and a small model can be the Andri Karpati nano GPD take that it's a good model and then you have a train weight also somewhere there really good thing print every tensor shape tensor is literally every collection of weights together so see what the weights are and what is the shape of it when I say shape it's going to come back like B T something right B is bat size T is going to be tensor dimension or how many tensors then dimension 4096

The Admin: Keep looking at that weight for every layer. Go inside and see that this layer has these many parameters. this layer is trainable. This layer has these many activation parameters. Right now verify one gradient by Nate measure how the loss changes. Literally that. So ask your cloud or someone to open the model load it send something calculate loss and ask the model to just go and change that weight and then see the loss. Look for yourself. This will give you a really good way of understanding how do we work like doctors. Now break gradient exclamation on purpose.

The Admin: Use the average with micro batches at different length and plot the curves and you can yourself see the issue that was there in 2024 and before that log the grade norm at every step see how the gradient norms change right look at the gradient norm changing for changing yourself compute your own MF MFU and if you're doing it in Google collab then you have a there good GPU for something like nano GPD so will be really little good now take the number 1.0 and write out by hand what it looks like in FP32, FA6 and FP8. I've already shared a table with you, but just spend some time on that table. It's super important and interesting for your future also. And then say which one would like rain and why, So that's all this transcript button doesn't work. People keep asking me. I just leave it there. the transcript I will have once the session is over and Google meet gives me the transcript. All right. Any question?

The Admin: We're getting very close by now you have full idea in different buckets. We have not integrated it yet but soon we are going to be on the integration side. Any questions you have? Yes, I think the next one is going to be a super interesting one. We are going to discuss Adam and Adam W. Then we have V dec.

### 02:00:00

The Admin: So next time we're going to be discussing how the optimizers are changing and what optimizer brings us what and it's not a historical thing but you still need to be aware of it because I don't know the answer. You have to help me figure out are we going to use Adamw Adam or something new or Leon and the new things that are there. I still not remembering the name. I'll figure out. Then there's a weight decay. Should we don't add it?

The Admin: we can't add weight if you're using reversibility. So we have that question also. I think I'll add reversibility here or it's coming soon. I think reversibility is not mentioned. I'll add it in one of the next two sessions. Then we have cosine versus WSD. How are we going to change the That is also important. Then we have EMA linear scale rule. Session 12 is where we have our massive interesting part where we have 0 1 2 3 memory map, multiGPU, then tensor pipeline sequence. Yes. I think next one should be the introduction for you for the reversibility. We had a hands up and hands down immediately. Okay. And we should be hitting 14 I believe. Okay. Any questions now?

Anirudh narla: If you don't mind me asking why did you say that this was irrelevant to quatization?

The Admin: Because we're not discussing quantization. A lot of people don't even know what it is.

Anirudh narla: Okay, sorry about that.

The Admin: And we may not be doing quantization at all in the course. You can ask now if people don't have question…

Siva Ajjapu: We are not going to discuss quantization.

The Admin: then you can ask a question. No, we're not on the inference side. We're on a training side, We're not making the model inferenceible. That's probably the session 20 or some student will take it up here.

Anirudh narla: Okay. Okay. Yeah. Nicey.

The Admin: All right.

The Admin: If you don't have any questions, then happy Raan to all of you. All of you can think of tying me or I will tie Raki to you. handle. You protect I protect you. I don't know. Maybe are you guys watching? at least spend three months with me. and that's going to be human writing so fast. Are you following this?

The Admin: It's on mute, but if you unmute it, you're going to see that a lot of kids are laughing, right? That's a beautiful place to be in. One of them is going to burn. Which One. None. No. I saw one of them burns. yeah, We just have this guy once. Yes. But just think about the audacity of a nation to conduct a humanoid Olympics and world will laugh. They will fail.

The Admin: But imagine the country of they are in the right direction right now and you may laugh today but they will laugh tomorrow when you will buy them your boss will buy them or somebody else will buy them. I think 10 lakh is the price point. Moment these are available at 10 lakh. Imagine it then you get an accountant, chef, a driver, a foot massager also at the same time head massager here. No salon. these are funny.

Raj H: Do you plan on teaching robotics also?

The Admin: This is how I like to fight. Raj I the plan is there but there's something that is missing.

### Meeting ended after 02:05:15 👋

*This editable transcript was computer generated and might contain errors. People can also change the text after it was created.*

