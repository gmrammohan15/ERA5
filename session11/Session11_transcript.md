## **ERA V5 Session \- 2026/09/05 06:43 IST \- Transcript**

# **Transcript**

The Admin: All right, today's session is on optimizers and learning rate schedules. I hope you enjoyed. There's a lot to cover and these are slightly complicated topics. So, we're going to go slow only, but I just wish you're as mathematically inclined as I want you to be today because if you are, then it's going to be a real fun because this is literally the GPS of what we're trying to build. If you can build this strongly and if you are aligned if you understand the deeper meaning of what we're going today, then you'll know what is exactly happening by learning.

The Admin: Apart from all what we've done, of course, the database is really good and the main thing falls here. We're going to be restarting our models so many times. We are going to be scaling the models. We're going to start with a smaller model, get some data from it, strain a bigger model, get some data from a bigger model. How do we align all of those things together? How do you make sure the small model is actually a good representation of the big model? Then parameter are the weights of the model? How does the parameter affect the learning rate and what is learning rate? do we need it for all the parameters? what happens to learning rate after we have trained the model? For example, if you're in RLHF or SFT, there's so many different questions that keep coming in and these questions are covered in a lot of different places but not at a single place where you can get all the details together.

The Admin: So that is what today's session is all about and probably on the last session before we actually start making the data set and start entering into the training schedule of our final run. All right. So in the last session we defined that the last session we defined that we have literally five lines of code and the last two lines are lost backward where we calculate the back propagation we calculate weight updates for all the parameters that we have and after that we do this optimizer step right and somehow magically all the weights updated today's session is to understand what is happening in that optimizer of step this is one of the most important step in the whole scheme of things and as I said think of it more like a GPS for

The Admin: each parameter, right? Someone needs to tell it where exactly is the minima and which direction needs to go. we do not know If we know how the minima looks like. It's going to be a surface where all the parameters will have a zero gradient because we get the best performance there. Loss is going to be minimum. So we will get a flat line there. But the point is that we do not know the location of it. We just know that It needs to look like a valley or some steep U curve at the bottom. We need to settle down. So we have We do know the direction of it, Think of it like the landscape I wanted

The Admin: imagine is that let's say you're on a sea u you do not know how far you are from let's say the port you want to go but you don't have a direction for it that's the scenario we are in and the port will keep on changing because as the parameters change our loss also keeps on changing right so we do not have a fixed location of where we want to go fix I'll say GPS coordinate where do we want to go so that's what we want to cover so some topics that we're going to cover today are learning

The Admin: rate what exactly it is then how does it help then the second momentum something that improves it further and then we have atom after that we'll talk about weight decay and other things that are going to come in map is a new topic in whole course never been covered earlier so we'll spend some time on that now let's talk about some terminology which we need to be aware of and we're going to be using a lot today the first is called learning rate is going to be allowing us to update the parameters that When we calculate back propagation that tells us the gradient is what? Rate of change of loss with respect to the parameter that is the direction it's not the actual change right we are using it as actual change. So there's a mismatch there and we're going to talk about that today. but the idea is that we know the direction using the Gradient anyways is Tangent for a curve is an angle.

The Admin: So we're getting an angle from there and we are using it to update the weight and that is why we introduced nea which is our learning rate to reduce the update that we're providing back because every time direction can be a big number. So we need to make sure that we're getting a good hangover we want to go and directions are all not always correct. For example on a mountain you will have a steep valley fair enough but there might be some stone in the middle right. So when we go near the stone the gradients are going in the opposite direction but ultimately we need to go down the valley. So then something needs to happen to make sure that we can actually sort of integrate the whole gradient that is pointing us towards the down valley. So that is where the updates of learning rates we're going to talk about the three things we looked at second momentum and atom that's where it's going to come. Then Hyperparameters are sort of numbers that we defined before we started a model.

### 00:05:00

The Admin: most of the hyperparameters are already searched for people keep publishing about and they are empirical in nature which means that people have done a lot of experiments so we'll understand from those experiments which one suits us for and for our requirement but it's something that we need to figure out before we start training the model now the hyperparameter selection used to be the most complicated thing before I'll say 20 16 kind of number and moment we had layer normalization and lot of regularization things this was solved essentially so now we actually have a set dictionary. We can go look at a dictionary and use it. But we still need to know about what these hyperparameters are. Then we have a Optimizer state is we

The Admin: We're saying that we need to know the learning rate for each parameter. That's fine. But as we learn about these parameter, we need to save them somewhere. They need to be in the memory so we can update them. and we need to have it for every parameter. And another way of thinking about these parameters are imagine that we have a missile that is going towards a particular let's say your city. then you send a heat seeeking missile to track it and then blast it out in the interceptor let's say you're making now if you just follow the velocity or the speed or velocity you're going to be in a direction where you think it is but it has some acceleration also so you'll miss it again which means you need to track its velocity and its acceleration right we need to track both the terms at the same time and if you track both then you're actually tracking the curvature and that is exactly where Adam and other things are going to come in where they don't not only track the velocity of the movement of the parameter they also track the acceleration to understand is it making a curve around a surface

The Admin: So that means that we need to maintain more than one value or one optimizer state for a parameter. So that's why we saw last time also that Adam states are nearly 2x the parameters. Again going to discuss that part. Then one epoch. This used to be a favorite term earlier. I've trained my model for epochs same data. We training the model multiple times again on top of each other. That doesn't happen anymore because you have huge amount of data and model gets really good by the time we actually end the data. So today these days we generally have one pass maximum 1.2

The Admin: to 1.3 passes depending on whether we have enough data to train or not not. And then we have a schedule is the LR schedule generally we speak about but it's mixed with some other things as well or maybe we have the length extension as in the part of the schedule but mostly it talks about how the learning rate is changing over a period of time. As we start a model it is all random. We need to figure out a way of getting it to a speed right immediately will not hit a speed light of movement. we'll move it to interaction and then make sure that from there it is training properly and as we end as well we need to fine-tune very few things right so we need to match that point we'll discuss about this as well but an analogy is let us say you want to go from your office to your home now maybe your average speed is 40 km/h if you're in Bangalore then it's going to be 10 km/h depending on what time of day you are in

The Admin: But you will not leave your desk at 10 km/h. It will be a slow start. You're going to say hi, hello, bye everyone, pee and then go to your car and then from there you're going to go out to the basement and then you're going to start at High speed of 10 km is big in Bangalore and after that you're going to reach your home. Now the way we update our parameters are we always give some sort of delta, right? This is the bunch or this is the meters you're traveling. Now you can see that in office You're going to be starting in centimeters and when your car is going to reach your house, you're again not going to be working meters.

The Admin: We're going back to cmters now. Otherwise, you cannot park a car also. So, you see that the scale of what we give to the parameters are different. initially everything is random. So, we're going to start fast. But when we're about to reach home or our minima or the value we want to stop, our learning rate is going to drop tremendously because now we're not tracking to move our parameter from 0.1 to 0.2. we are trying to move it from 0.23456 to 0.23459. 2 3 4 5 9 right so the delta that we are looking for is a 0.3 so that's why the LR is also going to go slow so we're going to discuss that part also so these are some of the things that we need to keep in mind any questions till now this is the introduction of what we're going to cover today all right so let's talk about gradient descent is a very simple rule

The Admin: where we look at the gradient and then we divide that from our current parameter that we have. So what we do is we assume that this is the kind of curve that we have for L versus W. this is L. This is where the loss is increasing and this is our W and let us say we are at some point here. is that W we're talking about. So we calculate a Gradient nothing but by delta W. Delta L is this how much the learning rate changed and delta W is how much the weight changed right that gives us a curve. So what we're doing is we are using this literally delta L by delta W that now it's on theta So this is theta we're talking about perpendicular upon the base. So you are doing this minus tan theta.

### 00:10:00

The Admin: So this should already bug you that tan theta really we are just subtracting the angle from it we should be subtracting some delta with it right but we do this and that's why this is a weird value this is a direction value just like you doing this you're doing 40 km minus south are we clear this is that equation that we just wrote 40 km minus south that is something what we're doing here do you understand the problem. We do not have any other solution for it So we improve it by the way the things we do. Are we clear? We're doing something with the velocity or the position or you can say if you don't want velocity here then you can say that this is let's say 65 m minus south. that's something that is something similar to what we're trying to do here. So tanka itself is not good enough but it does give us a direction of where we want to go.

The Admin: So 65 km minus south is literally telling us some idea, Or maybe 65 km minus left is what we're saying here. If that you want to be only in 2D, right? So what we do? is we multiply it by anita which is learning rate. We reduce the value further and that gives us a slow step of every time where do we want to go and slowly we essentially want to reach this particular point. This is what this equation does. Any question till now we're just going to make this equation complicated. So if you do not understand any of this you'll not understand anything further. I'll wait for 10 seconds.

The Admin: If this was a ISRO launch, the weight of 10 second is going to be this. 10 9 8 7 6 thank you. M How are you?

M: Yeah. Hi Rohan.

The Admin: Hi. that's…

M: So you telling that 40 km minus south, how is that matching? Okay.

The Admin: why I said if you getting confused here then you can look at this path. So imagine that this is where you are. this is 65 km. We are basically subtracting this from it. So we saying left that is easy to understand.

The Admin: Uhra Yeah,…

Ritambhra Korpal: Am I audible?

The Admin: you're able now.

Ritambhra Korpal: So, what I'm saying is if you're multiplying it with a number, it will still be a direction, but learning rate is a number.

The Admin: So learning it is a number. So think of it we are on an axis. this is where we want to be. We do not know the distance from this guy. But from this particular point let's say our milestone we know we are 65 km.

Ritambhra Korpal: Mhm.

The Admin: And that nita into gradient this is telling us left or right. Right.

Ritambhra Korpal: Yes. Yes.

The Admin: So now at this point it's telling us go left that that's all that is happening. And on top of that what we are saying is that we do not trust it very well. So we are going to make it even smaller by multiplying by na which is this value. But it's a math number…

Ritambhra Korpal: Yeah. But it is still 65 minus left, right, south, north, whatever, right?

The Admin: because tan theta is a mathematical number.

Anirudh narla: So it's direction which doesn't have a fixed value right variable when you say ta and…

The Admin: We are more interested sign of it.

Anirudh narla: and then multiplied by a constant named…

Anirudh narla: what is that okay variable itself okay thank …

The Admin: learning rate.

The Admin: It's not a constant but you can consider it for All right. So that's the overall idea. So that's gradient descent. if we have

Anirudh narla: Last thing so okay yeah is there any way we calculate these numbers like the learning rate?

The Admin: Got it you are in topic two we have…

### 00:15:00

The Admin: till topic.

Anirudh narla: Okay. I am.

The Admin: So this is essentially the gradient descent. if you have few parameters let's say you have 5,000 6,000 10,000 a million parameters then Gradient descent will also work if you have less data set and more samples, right? Gradient descent will also work if there are a lot of parameters which are dependent on each other. all of this is going to point to something like images. on images we have cars, they have similar Gradient descent work really well there. SGD which is gradient descent. Stoastic basically means the random thing that we're already doing here.

The Admin: So gradient descent works very well with images where we have convolution neural networks because each kernel there is going to be three cross let's say 32 there are thousand parameters which are talking to each other linked with each other so works in that scenario but the moment we go for linear layers which is what the full transform off LMS are built off gradient descent really doesn't work very well there because loss there is a function of billions of parameters and one parameter is actually dependent on other parameter They're not super tight but they have some relativity with each other. So right way of thinking this is going to be if you have a set of parameters that are linked to each other then gradient doesn't work. All of them can go in the same speed in the same direction.

The Admin: But if you have all the parameters if you have many parameter which not linked to each other which is the case with there's one parater learning science the other parameter learning philosophy and the other learning math for instance then they need to have their own independent movement on how do they want to move right so that's what we're going to be discussing it now moving further So this is gradient descent this equation essentially. Now take one weight starting at zero and let's say our loss is calculated like this which is 5 square. so if we make w equal to zero of course that we'll have big loss but if we make our weight equal to 5 then we know the loss is going to be zero.

The Admin: This equation tells us value immediately. One parameter we can look at it. We can solve Three parameters we can also look and solve it. But moment we have billions we can't even look at it. But if you take the gradient of this with respect to w. So we'll have delta l by delta w to 2 into w minus 5\. Right? That's the level of class that we learn. And this two is coming from the square that we had. So this is the gradient that we have right now. If you call the distance as d= w \- 5\. If you just call this d= w \- 5 and if you solve the multiple times w new for example which is going to come from this equation is going to be the old one that we have minus na the learning rate we had 2 coming from this side into 5 no problem.

The Admin: If you solve for it then you're going to see that you get to 5 \- 2 \- 5 and from there you're going to see d new is equals into 1 \- 2 n right so whatever distance we had earlier 1 \- 2 learning rate is going to be the step every time that we have so what this is telling you is each step is not going to be constant as you should know and it depends on higher the learning rate the new step is going to be smaller compared to earlier one. Smaller the learning rate the new step is going to be at least as big as the first step. Right? So you're slowly going to understand where this actually leads us to. So what essentially happens there if need here we taking as these values 0.01 and 0.10

The Admin: 1 0 and 0.90 and 1.1 as you move you're going to see over five steps as the Nita is increasing over five steps our distances are going to be changing like this right so for a small learning rate overall what the D new is going to be telling us is.129.39 point48 as you increase the Nita further you're going to see that actually becomes 1 1.8 2.4 2.9 3.36 if it is 0.9 you're going to see that already it's then drops to 1.8

The Admin: 8 7.56 2.1 so it's shuffling essentially and then we have 1.1 you're going to see that shuffles even more right so what is important here is that from this I've derived this particular table which tells you that based on the learning rate how much distance we're going to travel every time is going to change and that essentially is something that we need to maintain or we need to get that oscillation into control because if we do not control how fast each parameter moves we are going to skip landing at a home right so that's where the whole

### 00:20:00

The Admin: All the next section comes in that how do we control this behavior and the behavior is literally coming from us substituting d equal to wus 5 in this equation and then doing this a simple calculation. any question that the new one dependent on the old one into one minus two learning rate.

M: What to infer from that new equation? D into 1 \- 2\.

The Admin: That's all. You see this one 1 \- 2 NA is 1 uh 0.01 clear.

M: So yeah, you telling me that it will shrink and grow. Yeah. H. Okay. Yes.

The Admin: So 1 \- 2 into 0.01 is what?

The Admin: Is it clear? That's all. And if you use this and you calculate W again and again, if you calculate this equation again and again five times, the first one, you're going to get this. This is how W is changing. So instead of showing you the full math, I'm just showing you a simple. And if you're confused where this five came from, this two goes inside becomes 10 and one of the five comes here. Right? So we have 15 in the current step we just seeing…

Dattatreya Manjunath: so even multiplier which is ea we are basically trying to find a value that is u minimizing the oscillation right so somewhere in between 0.1 and 0.9 is that what we're trying to do Hey.

The Admin: what you're saying is that if you fix it, this is the behavior right now where we'll see we are seeing W fluctuating very fast.

The Admin: We discussed W has to be five here. Right.

Dattatreya Manjunath: Yeah.

The Admin: We discussed W has to be five here. But if you pick Rita 0.01 0.1 1.15 1.1 this is how the W is changing in next five steps. So 0.1 we still read somewhere here. 0.9 we've already shot it and we actually shot it much before.

The Admin: So we've already started oscillating. So it needs to be maintained well so we can slowly reach our point our value of five and W over five steps.

Anirudh narla: So just wanted a quick clarification. So the step essentially represents how the weight changes right?

The Admin: The value of W in the night next five steps W starting from Yes.

Anirudh narla: Yeah. So the change of the weight itself within the next five

The Admin: Seven.

Siva Ajjapu: So what are the negative values here? So I could see the negative values on the screen.

The Admin: What is this value?

Siva Ajjapu: It is the maybe summation of all the five values. that. Okay.

The Admin: more this is equals to this.

The Admin: So 1 \- 2 into 0.01 Are you this is equals to this 1 \- 2 into 0.9. What is this equal to here?

Siva Ajjapu: negative of 8\. Yes. Mhm.

The Admin: Okay. done.

Siva Ajjapu: Yeah. Thank you.

Vardhan Walavalkar: Yeah.

The Admin: I lost you.

Vardhan Walavalkar: Can you hear me? Okay,

The Admin: Yeah. Word.

The Admin: I'm again losing I'm sorry I can't hear you. Can you write down if you get time? So all of this exercise all the math behind is to show you that how does the d change and based on that how the w is going to change. Right. So d new is dependent on d into 1 \- 2 learning rate. That should tell you that how much I move right now. So let's say I move 10 km right now and my learning rate is let's say 0.01. The next update is going to be 0.98. So my multiply is going to be 0.98. Which means if I move 10 km right now The next step is going to be 8 into.98 km. Right?

The Admin: But if I was moving with nita equal to.1 my movement is going to be something like8 right which means if I move 10 km in this step next step is guaranteed to be 10 into8 which is 8 km the next step is guaranteed to be 8 into8 which is 6.4 km and so on but if I pick the learning rate is 0.9 then I have negative of8 which means if I move 10 km right now in the left side the next step is going to take me back 8 km and next step is going to put me forward 6.4 4 km. So you can already see I'm oscillating essentially there. If I make it 1.1 then you're going to see the update is going to be negative 1.2. So if I move 10 km in south the next step is going to be 11.2 km in north. So where I started I've actually moved 1.2 km further there and then I'm going to doative 1.2 again. Right? So I'm going to move on this side again. So I will keep on oscillating. Is this analogic clear? What is happening in this particular table?

### 00:25:00

The Admin: This whole thing is just to explain you that if you pick a learning rate just like that as we have done here, it's just going to be oscillating. We want to be slowly moving towards where the loss is loss is going to be zero which is let's say five d= to 5 right or w equal to 5\. that is only for one equation here we had only one parameter. We have w minus 5\. So we already facing this particular problem where we need to make sure that our learning rate is small enough so it can take us to the valley. let's change it to two. moment we have two and we have this new equation into 20 U² \+ V square. We have two parameters here. if we were to do all of this calculation for this you're going to see that we have a curvature which is 20 along the U axis because we have 20 in front of that. whatever update we were doing here it's going to be further multiplied by 20 because we have this 20 in front. Right?

The Admin: And this is how our landscape is going to look like. And this is how big this is where u and v have same multipliers. So you can see u ² \+ v square. But as you increase, you're going to see that we have one axis getting squished and other axis which is longer. If you follow what we were doing earlier and we were to calculate for this we can figure out a good learning rate for let's say our u axis because now it is smaller 50 times but that will be 50 times bigger for the axis right it's a big problem we do not have these constants in front of all the parameters in the model every parameter will have a of constant in front different kind of effect on the overall learning rate that is what we're trying to say here that u is affecting a learning rate 50 times

The Admin: more U square is affecting a learning rate 50 times more compared to V square right and if we try and figure out what we just did here good learning rate for our parameter that is definitely going to be off for some other parameters is this part clear that is all what we're trying to show here that if our loss is dependent on parameters with different rates we cannot have a single learning rate which is going to allow us to hit our minimal value faster or even at all because you may have selected Good learning rate for something that is moving fast or something that is far off it will never be able to reach it will just stay there. Any questions or not?

Dattatreya Manjunath: So in this case the learning rate is going to be somewhere in between what would be the ideal learning rate for the two parameters right?

The Admin: Correct. Some not somewhere in between.

Dattatreya Manjunath: Got it. No.

The Admin: That is exactly what we're saying that we do not want it to be somewhere in between. We want it to be decided for each one of them. They need to have independent learning rates. Think of it like you have event going on there. you have called the caterer from Bangalore but you have called the tent guy from Delhi right they cannot have a same speed towards the event the Delhi guy has to leave early and he has to probably take a flight to move fast so every parameter for the event or every person or every company that is coming in to make that event has to move at different speed so all of them can reach at the same time Nan

Dattatreya Manjunath: Got

NITIN YADAV: Yeah, Rohan.

NITIN YADAV: So, you mean to say that we have different learning rates for the U and V and those learning rates are also a variable across the steps because they will change once how we move. And how exactly we select the initial learning weights then or we are going to cover that.

The Admin: 100%. Yes,…

The Admin: we're going to cover that.

NITIN YADAV: Okay.

The Admin: So what we have till now figured out is that fixing a learning rate for example nita here is going to give us a multiplier for the next one which is 98.8 G.

The Admin: 81.8 1.2. So that gives us a good direction. We definitely don't want negative otherwise we'll be shuffling but we want something that takes us slowly to our learning rate slowly to a minima. Then we also looked at this chart which is telling us that if we have different relations of parameters to the loss then we need different learning rates for them because we want all of them to sort of reach our minima at the same time. Right? That is minima where all the parameters are minimum. And when we say all we are saying at least 95% because there are some parameter that we cannot satisfy that you can't make everyone happy. So what we have done is we're talking about learning rate here as we change the learning rate you're going to see that oscillation that I showed you here in that particular table this 9 1.8 7 and these varying number is what is showed in this particular graph.

### 00:30:00

The Admin: So as you increase you're going to see that you are not going in the direction you want and as you reduce it further might switch in other side. when the learning is very small you're going to see that it's actually very slowly and if I were to not have five maybe 50 steps you're going to see that it actually crawls towards here. So that gives a very good idea that if the learning eventually you will reach your point right. But the learning being very very small means that you have a lot of money. You have lot of big numbers of GPU which you can push. So you want it to behave slightly in a manner where gets you in the direction faster. Right? And these are only five steps and after that you have more. But if you cross that chasm where you're not balancing it out slowly you're going to see that the oscillation starts. And here you can see that till at least this particular point I was in control.

The Admin: something like that. All right. So, we need to find this kind of point where I can shuffle faster and reach a point. Are we clear? The same table which was shown here is now converted into a Meaningless graph but just to show actually what happens when we train a model. So very small learning rate. We have very slow descent towards where you want to go. But as we increase our learning rate, we start seeing these oscillations and then we actually can go out of control. Are you clear? This is literally designing the suspension of a car, If you design the suspension of a car for a particular pothole, then it will work in that pothole, but after that you have a speed breaker, especially Bangalore, So you have a pothole. So I read somewhere on Reddit that people who design speed breakers are the one the contractors who should be given the right to design the road also because roads are f\*\* up but speed breakers are perfect in Bangalore.

The Admin: anyone who designing street breaker they're doing a really good job it's perfectly shiny crystal no dent at all after 50 years of uses also it just remains exactly at is but everywhere else you'll see potholes right so idea is that when you're designing a suspension you cannot design for a single hole you have to make multiple port holes into consideration. So now we have the momentum part. This is precisely where your intuition should start coming in. if at one step again heatseeking missile think of what the heat seeeking missile is asking you.

The Admin: What momentum does is if you know that you're moving in the south for the last 10 steps you take a risk of taking a bigger step in south right if the direction is constant for some time then we take a big leap of faith and go in that direction right and that allows us to essentially solve this problem how do I know that I'm going in this direction till now for example right I know I'm moving this direction. So is there a way in which I speed I can go further in that direction. Right? That is what momentum is trying to do. So in momentum we keep exponentially moving average. What we do is we take here is shown and that is a delta. Now we're talking about how much we changed. These are not weights. Keep that in mind. So m is the last change that I had which let's say 5 m in south that or 5 m forward is what I know.

The Admin: I'm going to take 90% of my memory, 90% of the last value and only add 10% of the update. Right? So this 1 \- B1 is the same value that we had here. this 1 \- B is going to be So 10% of the new valid is coming in. Right? So I believe on my pass updates much more compared to the current one. Now why this works is first of all you see 90% and 10%. These are sort of constants and people have figured out and that's why we see this point.9 a lot of places this is empirical value sort of a stable value which people have found over last 20 years of experiments you can tune it to make it 91.89 but for that you have to run your model multiple times to see which one works well. So that's why it's empirical value that is sort of guaranteed to be around 0.9 always. So we take 90% of the history and 10% of what is coming in.

The Admin: Why that? sometimes you get a noise. You get a sample suddenly that makes no sense, right? So some data came in which is trying to screw all the parameters. and not letting us go in the correct direction. So in that case it can only affect us So we not going to be if the sample we are training on is wrong then it only affects it by 10%. But if the sample we are training on is correct then the direction we are going in should already be the direction we should be going in. So we do not let a bad sample affect us that much. Are we clear on this on what is happening here? We keep and this is exactly how we calculate where the So today let's say stock market drops by,000 points. Now should we just leave this country sell all the gold basically sell everything that we have convert that into gold? today it fell thousand.

### 00:35:00

The Admin: Yesterday Before that it again fell,000. But there was a time when it was going good. So in that hope that things are still good in this economy, we'll probably maintain our stocks. this is a learning rate which is again 9 What we are seeing here is we have a direction for U and we have a direction for V. Right? So now we're back to our two example. here you remember that we had U and V. We're contining the same example. So we have two parameters now and we are trying to see what momentum does to those two parameters and we also discussed that one of them is 50 times bigger than the other and square of them. So we need to have slightly different learning rates for both of them. So we're trying to solve that problem using momentum. what we're seeing here is and same math that we used earlier is now being used here. We have u and then we have v Here we have 20 \* meter and we have here we have n.

The Admin: This 20 is again calculated based on u 1 minus ba how much of the old value we are maintaining right this is going to come from the math or the equation that we have directly in later on but that's what we're seeing now as we change the learning rate you're going to see that both of them look at the v part that should be very clear right in the momentum we have one and then 98 and 84 so that is how we are calculating the old value but look here momentum is essentially trying to average things Here the learning rate is fast but as we go for a smaller learning rate we're going to see that momentum allows us to keep that value also in check. Both of them are sort of coming down as less oscillation as possible. Are we clear on this 1 \- 20 n we have a 20 times bigger learning rate here compared to here. So if we were to and this is 20 times bigger because we saw that one value was 50 times bigger effect on the loss.

The Admin: But if you have momentum that both of them sort of get in direction you can see immediately become straight right and also it is way less fluctuating compared to if you don't have momentum any question on this okay Now 11\.

NITIN YADAV: Soon I didn't get why we have 20 for u 1 \- 20 it's normally 50 times …

The Admin: How big is you compared to V here?

NITIN YADAV: but we have to consider the square thing also.

The Admin: I can solve it for Delta L by delta U is what?

The Admin: 50U I didn't get the question delta L by delta U is…

NITIN YADAV: 50 into 2\.

The Admin: what here two goes out kills the half…

The Admin: then we have 50 U and then we have delta L by delta V here which is what U V we have some bigger number in front of U here right that's all we are saying that 20 is not significant here I mentioned that there's going to be some equation that is going to finally help us get that exact value…

NITIN YADAV: Y yes.

NITIN YADAV: Okay. Okay.

The Admin: what is that value going to be don't link this 20 with that 50 there's going to be big number here because we had 50 there that is what I'm trying to share because if I mention

The Admin: is a 50 then you'll remember we have to figure out that relation is not clear especially in multivariable equation but we just know it's bigger one okay so what here we are trying to see is if we have a small learning rate same thing as above right what we saw here if you have a small learning rate we saw this and we need to see this grainy descent in two dimensions so at this particular point we have one starting at and this is where we want to reach as increase

The Admin: learning rate we see that we get this fluctuations right now same if you see for two parameters here we have u and here we have v if we now move this you're going to see that bigger learning rate might allow us for one particular shallow direction but other direction just floats up that is what we're trying to see here had we had momentum here then we might be able to basically see the left and right and left and right let me average it out to the Are we clear? What are we trying to show here?

### 00:40:00

NITIN YADAV: Okay.

The Admin: So in the shallow axis we are always positive. So we always going here. In the axis where we have a bigger movement, you can see we plus \- plus \- plus we had momentum plus minus would have averaged out. that is what we're trying to extract from this particular one. And this one is trying to show.

The Admin: Here we have the oscillating 1 2 and two and then we have a steady number and both of them are dependent on how we are handling our momentum. Now this one is showing with the momentum right the actual numbers are moving us in very very different directions but if we were to take a momentum then we will be able to reach that particular point without many oscillations. So compared to 1 2 3 4 maybe 50 oscillations or at least 15 oscillations here. Yeah, we are reaching the point in we are meeting this is dampening essentially right we're dampening the oscillation that we need that we get that is what momentum does for us. So we have learning rate first of all we have a gradient gradient is nothing but left and right then we add learning rate to it because otherwise the left to right can be a big number. We want to maintain it. We want to make it smaller. Then we realize that if you have two parameters and both of them have a different effect on the learning rate then we need to have momentum.

The Admin: momentum is at least going to dampen this particular effect. We have still not spoken about both the learning rates being different yet. We still saying same learning rate 20 Nita and one Nita. we're trying the Nita is fixed right 20 we figure out but it's a constant for the rest of the life and Nita is learning great for all the parameters. So momentum does help but again still not good enough for Any question here?

The Admin: Okay, let's talk about per parameter learning rates. And this is exactly where Jeffrey and other people started contributing. And this is where literally we had a breakthrough for our linear layers because till this was discovered or till Adam and RS pop and others came in we had SGD and HGD never allowed us to train with anything big because it was designed for scenarios where most of the parameters are linked to each other which is convolution neural network. So it worked very well there. all the things we learned momentum and learning rate and oscillations and everything that work really well for convolution neuronet networks because many weights are linked there in linear layers or our linear

The Admin: linear or if you have looked at the code in the last couple of sessions yourselves or perceptron when we look at a perceptron layer right these are different names of the same thing which is a linear layer or fully fully connected layer here every parameter is independent right every parameter is trying to learn something from the dimension that are coming in so moment that happens we need a per parameter learning rate and this is where the things become very difficult because per parameter Okay, if I have 1 billion parameter, then I need 1 billion of them, And again, we discussed that we just can't follow the velocity. We have to follow the acceleration also. So moment you have velocity and acceleration, then for each parameter, we have to track it twice. And that is where the RAM and Nvidia became a trillion dollar company. what happens in perparameter learning is momentum is still going to help us, but it still leaves everywhere sharing one learning rate, right?

The Admin: Even though we had 20 into nita that nita is still shared right and if I chain nita then it's fixed for everyone we had it here right so assuming that we are starting with 1 \- 20 n for one parameter \- n for other we have tried our best to link the magnitude of a parameter here the equation is different magnitude is 20 let's say we add that here the point is that the need is fixed So if I change nita as the model is changing I'm changing it for all the parameters and on top of that we have a condition or situation in LMS that we do not

The Admin: have same number of examples for same classes right in SGD or in images when we use convolutional networks we will have 10,000 images of cat 10,000 image of dog 10,000 images of elephants we have same number of examples also there was no scenario where no image was shown and we were trying to ask the model what do you think that particular object is but here we are doing literally doing that we are saying that you may not be shown a sample but you have to interpret based on different information so there are weights that will never touch let's say quantum biomechanics So quantum bioysics kind of concept but still we have to train that particular parameter right sometimes maybe one or two examples might come in and based on that this parameter still has to update what it's trying to do. So the point is one learning rate cannot meet the requirement of all the parameter that we have in the model. some parameter will be updated much less. So we need to figure out how do we solve this particular problem.

### 00:45:00

The Admin: What we do is we compute the gradient from its own history right we somehow try and link the gradient with respect to its own history what do I mean let us say there are 10 gradients and let's say there are 10 gradients and these gradients are not even 10 let's say we have three gradients And this is going to be updated 100 times. This is going to be updated 10 times. And this is only going to be updated two Next rest of the times I'm not getting updates. When I say I'm not getting update, I'm not saying that we will not calculate delta L by that delta poor parameter. We will calculate but this is going to be very very close to zero because nothing has come in to explain that particular parameter or the link with the loss. But This is a good history that we have. This is fine.

The Admin: So I'm going to keep on updating based on whatever is coming in. This is short. So it may not let me reach wherever this parameter had to be. And this may be very very short. Right? So the idea that people took from this is if I'm not getting an update, can I still use the old update again? I'm not getting anything from the parameter right now. The loss is not helping me to figure out where do I want to go, but can I still move it? And that is us learning from a history. Last time my loss wanted this parameter to move in that direction by that amplitude. Can I continue on that? So if you were to maintain velocity and acceleration both velocity and acceleration both if you were to maintain the acceleration and suddenly for some reason the velocity didn't come because we didn't have that sample in the learning. I can use my acceleration to figure out at least p what vcap would have been and use that to continue to update. Are we clear on this concept?

The Admin: Right. What you need to understand is that a neural network or the parameter that we have they are very similar to the sensors that we have for example In aircraft we have this suddenly our GPS satellite that is in the air is not able to send the signals to us right and we still need to figure out what is the step I should take. So what do we do? We figure out our acceleration. We figure out where the last GPS location was and try and interpret where I should be based on that and jump Very similar to a noisy system that is actually a drone flying in the sky. Everything is noisy. I do not know the exact GPS signal. And if you've seen the fit saga then that US can actually send your aircraft to 50 m off also. So we still have to figure out exactly I am and where I can go and that we do it from the history that I have.

The Admin: So a moment a parameter moving in a specific direction doesn't get an update we can look at the past update and move it right and also if we have one sample in a batch of let's say 1 million tokens and only 10 tokens were related to a particular parameter you can see that even that amplitude is also going to be very small so we reverse that if the amplitude is small let me train it with a bigger multiplier for that amplitude so I'm actually getting enough information from that small sample So the rule here is essentially the parameter that get a lot of updates their amplitude becomes small for us when we train them and parameters that get very very small of less times updates. So this is very small we increase the amplitude there. So amplitude becomes bigger there. That's the rule that we follow and this works magically well. Right?

The Admin: So parameter that do not get enough updates or parameter that get updates which are very small in amplitudes again when we say mathematically by binding history we mathematically increase their amplitudes and parameter that get constant updates constantly get screamed out for example than is a word that is used trillions of times in our training schedule we make the updates intentionally smaller because those are getting so many updates they're actually Any question on this? Because once I remove the screen, there's a math behind this. Today is the only math session and I know is Any question on this?

### 00:50:00

Avnish Midha: Yeah. Ron, I was when you say amplitude, it's the Anita, right? Okay.

The Admin: Amplitude is the neater. Yeah.

Dattatreya Manjunath: So when you said we need to keep track of acceleration along with this is it just increasing the TA series expansion that we do from one degree to two differentials rate of change of detail.

The Admin: No rate of of nita itself. Rate of change of weight itself. Rate of rate sorry let me explain.

Dattatreya Manjunath: Yeah. Right.

The Admin: Change of loss is gradient. rate of change of loss.

The Admin: with respect to the weight is the gradient. Correct? Okay.

Dattatreya Manjunath: Thanks. Thank All right.

The Admin: Rate of change of the loss with respect to the gradient is the acceleration of the loss with respect to the weight. the gradient. ta L by delta G is the acceleration. So that's the acceleration. If this is G,

Dattatreya Manjunath: So, yeah, it's basically just that, right? Got it.

The Admin: And…

The Admin: these parameters help us change the Nita of course is going to start from some value let's say 0.01 right but we have multipliers in front of it. these multipliers essentially change ordinary

Swati Bansal: So I'm trying to understand the intuition here. So basically the words that do not occur very occasionally for those words the learning rates are kind of amplified. but at what point does the optimizer do it like it has to complete the training…

Swati Bansal: then in order to know that the words will not come right because it has not seen the whole training set. So I'm not sure how is that working behind the scene when does that get applied?

The Admin: …

The Admin: think of it like Let's say the weight updates are this. Very small. what we are saying is that if the weights update are small, we'll take a leap of faith and actually move it further. done. Optimizer does that.

Swati Bansal: So optimizer does that.

The Admin: Imagine that we have to be here.

Swati Bansal: 

Swati Bansal: Okay. Mhm. You're right.

The Admin: Moment our weight is here the next time immediately we know that we have taken a wrong step. We should have actually not taken such a big step. So next one would have move somewhere over here. So that still behaves in the way we want.

The Admin: But because now we have momentum and then we are tracking the acceleration also we can see this in multiple steps and see that essentially average it out right we can see that I'm going in this direction so I know I need to be bigger…

The Admin: but why can't I just average it it's like a ve addition of two vectors so I'm drawing this vector here and I'm drawing this vector here right so I'm just drawing this vector directly so this is what is going to be coming in from the overall equation so first few steps are going to be jiggly they're going to be massive that's why the first learning rates are very small. We try and figure out the balance where I figure out these directions faster because I know I'm starting at a noisy state. But that is where the overall sequence of updates comes in. When we say acceleration, when we say weighted average, when we say velocity, we say momentum, we're definitely not talking on one step here. For us to be able to even calculate this, we need at least 100 steps, right? So the algorithm we discussing stabilizes the overall process over a period of time.

Swati Bansal: the neck. Mhm.

The Admin: It's not immediately that I have the grounds. Yes, exactly.

Swati Bansal: got it.

Swati Bansal: So what you're saying is over the period of time these learning rates change depending on how they are learn the model has learned.

The Admin: So this itself is a actually statistical model that is getting updated.

Swati Bansal: Got it. but one thing also last session we talked about the cost right because the more amount of time it takes for training u u with a smaller learning rate it is adding to our cost right…

The Admin: Hey So you'll not believe the whole world has converged between these numbers.

Swati Bansal: but at the same time u so if the oscillations occur we are having a counterproductive we'll never reach that loss right so that's what we were saying that we have to find that fine number and all these algorithms are around to find that perfect learning Mhm.

The Admin: In fact, not even this somewhere over here. So^ \-3 to 10 \-4. Every single new network starts here. that's given.

The Admin: And everyone now use Adam or Adamw depending on their religion literally most of the times have Adamwin fashion. Now we pick this this is a small learning rate this is the highest learning rate we have. Sometimes we go to 3x sometimes we go to 4x also but that's a cap that we have after that we just believe that this guy is going to fix everything for us. They are so good that even if this value is big or this value is small, it will automatically adjust based on…

### 00:55:00

The Admin: how fast the parameter is updating. So we just give it a max learning rate after that and max learning rate is a We are talking multiplier here. NA ma into this value or what actually that value is based on the parameter moment how fast it is updated is calculated every single step. So even though we think it might be 3 into 10 minus 3 this might come back and…

Swati Bansal: Mhm. gone.

The Admin: say no routine you need to be 10 \- 5 further.

The Admin: So this is going to be multiplied with this and we get 10 minus 8\. Right? So we only adjust the outside box but inside box is handled by the algorithm itself.

Swati Bansal: Okay, cool. Thank you. Yeah.

The Admin: That is why when you go online you're going to see that we still for Adam and still mention a learning rate. Right? Let's go to Pytor Adam. There's a website called Pyarch. Are you aware of it? how many of you have gone on a PyTorch website? This is called documentation. There used to be a time when humans would go on such pages and read. And if you see here, we have a class thing in Python. then torch dot dot is something that is used to fetch something from that module. Torch is a module.

The Admin: A module is nothing but a Python file. And inside that we have a function or a class here Inside the optimizer we have this atom as a class.

The Admin: Right here we have parameters which parameter do you want to update and do you see this learning rate so we do have a learning rate so that is the learning rate that we supply we say that that's a max learning rate for us this then gets multiplied internally with a lot of signs to figure out for each parameter what this value should And then we have two betas here that we are just going to talk about. So that's a cap but that's I'll say not even a gap that's a line where we are comfortable to start a model and Adam decides for each one of them it's a 01 or a 01\.

Swati Bansal: So you think it's a max and…

Swati Bansal: not a minimum?

The Admin: It's not even a max. That's why I'm retracing…

The Admin: what I'm saying it's a baseline. It can go down.

Swati Bansal: Okay.

Swati Bansal: Okay. Thank you.

The Admin: most but it's still a baseline. It's not the max not discussed yet.

Anirudh narla: So the theory behind Adam is like a conjecture. It's not proven. Okay.

The Admin: All So First we discussed that momentum is going to take the averages of the last few things and give us a concrete direction. Right? I'm screaming left, then I'm screaming right, then I'm screaming left. Right? So I'm changing the amplitude also. I can average that out and say left in that direction, Instead of oscillating. So momentum helps us stopping that particular oscillation. Then we'll discuss the per parameter learning rate based on how the parameters are and based on how much they have moved. I can believe in the history and follow that.

The Admin: So this is what we're saying The V here and G we have a G square also. So let's leave this a bit. The weights of the model are also called parameters. And the fix is to give each parameter learning rate of its own computed from own history. So the learning rate for each parameter is calculated from its own history multiply by that 0.01 the baseline that we have. We keep a second exponential moving average here and this time over the squared gradient. So we take the gradient and square in why I'm calling it acceleration because in acceleration you have let's say u d s\_ub\_2ide by dt² right now t is there time but here time for us it's step and each step is just one. So we can just say that the square is also acceleration here. So what we're doing here is the v v new that is beta into v the old velocity you have plus 1 \- beta2 into g² right and that is acceleration at half. So that is what we're following here.

The Admin: So B1 and B2 are almost always above 0.999 and that's again something that comes from empirical evidence right so essentially our overall update now becomes w minus mita divide by vg right this is the value that we're tracking now so now v is dedicated to w v is married to w here we have this V and that V is now we have this V new it's called new

The Admin: actually right so this new is calculated from B into old new is going to start at zero as we start the model 1 \- B2 and as we discussed that it's actually a big number and G square so very small amount of acceleration right so I'm believing in my old value a lot but I'm letting the acceleration also change where I want to go so if G square is really big and continue to be big then only it can affect me so now the parameter the learning rate or the gradient update for us become the same as we had earlier but divided

### 01:00:00

The Admin: mu right and then we have G here because if I multiply G directly here I'm going to get my weight update any question on this g is the gradient here yes or no okay to further clarify why divide by nita here look at this particular table we have a parameter that is a value one and we have another parameter which has the value of 0.01 and this is the gradient that we're looking at right the gradient came as one and the gradient came as 0.01 the V if you calculate directly from that equation is going to come as one for this guy but for parameter V is going to come as 0.01 right its own learning rate NA divid by V is going to be 1.0

The Admin: zero and it's going to be 100 m and the resulting step where we do ng by new we going to get one and we're going to get one. So based on how small the gradient was coming in this equation allows us to balance out each of the update that we get right. So what you need to remember is this term na by v is something that is allowing us to the weight change the learning rate for each one of them. Are we clear? By the way, none of this is something that you should not know, but this is the maximum complicated thing that we're going to be discussing. So, we is equals to weight old minus learning rate into gradient. Are we clear on this particular equation? Say yes or no.

The Admin: New is equals to weight old minus nita / new into g. This 1 by new is dedicated for each w0. So we have to track this 1x v term for every single parameter. Are we clear? view new is coming from new old minus let me follow the term I lost here by the way I made something like

The Admin: Okay, this is one of my special thing that I spent a lot of time designing. So this B is 0.999, right? Which means 1 minus P is going to be 1 \- 0.999. So it's a very small number, right? So V which is our V new is equals to beta very close to one only. So 0.999 into V old plus 0\. We can just calculate right 0.0

The Admin: 0 01 into g² g square is the rate of change of acceleration right rate of change of loss of gradient itself so that's why we are tracking that particular value now v is equals to u \+ a t how many of you remember this equation right similar to that equation right that you're seeing T here t is step for us. So that is sort of one acceleration is what by dt itself right or if v minus u / dt right. So that is for us.

The Admin: So it's very similar to that particular equation but we are adding how much of that we need to take because again we want to believe on momentum we want to believe on our position on how we're moving. So till now what we've discussed we discussed the gradient descent which is a simple calculation or simple way we learned here that in a normal term if you just look at the equation that we have for a square loss this is the multiplier we're going to get for the next update. So if I move 10 the next is going to be 9.8 8 if I increase my learning rate if I move 10 km I'm going to be moving 8 km if I increase my learning rate further 0.9 I'm going to be moving 10 km then negative 8 then negative then positive 6.4 then 5.6

### 01:05:00

The Admin: six and So oscillation is going to happen. we are not happy with that oscillation. Then we discussed that in fact there are many parameter that do not have a same relationship with L, sometimes just 20\. It's so there are big weird relationships that are possible. Then we discussed that gradient descent in two dimension is going to look something like this where we are trying to go close to our minimum but based on how big the learning rate is we might be in The same table shown here in a widget. Then we discuss In momentum, we can contain the direction that we want to go.

The Admin: Basically, average it out and get a correct direction. But here, what we're seeing is that we have two learning rates. This is momentum not shown here. In case of a bigger learning rate like 1 minus 20, we are going to oscillate a lot. So, one learning rate is working for this small guy, but the other learning rate is not working for this guy. So, we have to get a learning rate which works for both of them. A small learning rate is allowing me not to oscillate for the \- But now my shallow term is going to be very slow in reaching. We are already here for this guy but we are far off here. And if I increase the learning rate I start seeing oscillation and now my shallow can reach but my other diverse. So we cannot have a same learning rate for both of them. So momentum does help in that specific case. Momentum essentially starts to stabilize the oscillation in a specific direction. Right? That is what is shown in this particular widget.

The Admin: Then we discussed that we need to have a per parameter the oscillation can be stopped but still it cannot stop the fact that if you do not have a parameter learning rate the 20 nita kind of value or the parameter that has a strong affection with the loss we'll get a big value but the other parameter which are small in nature get small update they will never get any update. So the fix for that is to maintain this one by v for every parameter 1x v is directly coming from the parameter itself right. that value is coming from the weight or the gradient term itself. So now I know that I actually have a very small gradient coming in. Right? How do we make The value is small. So we take one view one by the gradient itself. Are we clear on this? It's a very simple thing. because it's math I'm sure that all of you have started shutting down. This is V. Can you see this is V? Yes. No.

The Admin: I want someone to talk to An will talk to me. An I asked a question.

Anirudh narla: Sorry, but I am confused. I think I'll have to rewatch this video.

The Admin: What is this?

Anirudh narla: New 0.01 1.02.

The Admin: It's called new.

chirag Tagadiya: We

The Admin: What is this? me anything 0.01. give me another value for it which is let's say more than one 1.02. Perfect. So this is and is new B for two different parameters. Say okay.

Anirudh narla: Okay.

The Admin: So this is for W1 parameter and this for W2 parameter. Say okay. Okay.

The Admin: Here tell me where is new coming in numerator or denominator numerator.

Anirudh narla: Numerator Okay,…

The Admin: So I am going to be writing this as 1 / 0.01 01 for our W1 weight. And I'm going to be writing this as 1 divid by 1.02 for our W28. Say What is this value now?

Anirudh narla: that is 100 some 0.98 something.

The Admin: What is this value Close to one. Right? This is 0.98. Correct? So…

Anirudh narla: Yes. inversely proportional.

The Admin: what did we see that when the new was small because it's used in denominator. Why was small? New was small because the gradient was small.

The Admin: New itself is coming from W gradient gradient updates. Correct? So we have an inverse proportional relationship already. So if the gradient updates were smaller one by new automatically is going to be bigger. If the gradient updates were bigger it automatically going to be smaller. Are we clear on this now?

Anirudh narla: This is what you meant by the nudging.

The Admin: This is what I meant by that the gradient updates are small one by small gradient is a big value.

The Admin: So we automatically get a bigger learning rate for that.

Anirudh narla: Got it.

Anirudh narla: Thank you.

The Admin: What do you mean this?

Keshava Murali: Yeah. I was just curious to know why did we have this square term g square? I understand it's acceleration but how did you get a square in 1 \- b2 into g² u the equation for new b2 yeah yeah this is the gradient.

### 01:10:00

The Admin: What? Yeah, because we are saying that this is more like what is G here?

The Admin: gradient. Okay.

The Admin: So what we're expecting is the g square is going to act like an acceleration for us. So we are saying v equ= to u plus a t. So the new v should be dependent on the acceleration. if the g is very small the g square is going to be even smaller. And if g is big suddenly I get a bigger update. So to handle such situation.

Keshava Murali: Okay.

Keshava Murali: Okay. Okay. Thanks.

Dattatreya Manjunath: Why is it 1 minus B2 and…

The Admin: Again coming from the fact that we want to rely on the history a lot more…

Dattatreya Manjunath: not beta\_2? but we don't do that. Gotcha.

The Admin: and in fact it's what is B2 here 0.00991. So I'm relying a lot on my history compared to the certain term This is to get rid of all the wrong example that might come in. What you need to understand here is

The Admin: No, no. What you need to understand here is if you look at this as a single term for a single step equation, it will not make sense. You need to tell yourself that I have run this times. If I run this thousand times, then the V is actually giving me a good direction. It's a signal lock that I already have right now. Suddenly there's a G term G square that is coming in and that is a big oscillation. is saying that it's like a missile going to Pakistan and you're telling the missile no Pakistan not that side that side because something some jammer came into picture so how much should I trust the new information so here we are saying we're not trusting the new information because I trust my last thousand information more That's

The Admin: It's 0.991. So I'm trusting my 999 histories compared to the new history coming in literally Swati.

Dattatreya Manjunath: Good.

Swati Bansal: But isn't that the gradient clipping con concept that from the last session you taught us right the gradient norm and…

The Admin: No no no completely different we are going to talk about grading this is clipping is completely different. don't…

Swati Bansal: it's mentioned that we clip the gradient we get a bad batch when we don't want the effect of a big sample to spoil our loss Right.

The Admin: since you're in talking about it. gradient clipping is what?

Swati Bansal: So we just the norm.

The Admin: And what do we do there? We clip it to one. Yes.

Swati Bansal: Yeah. we divide that by the scale of the Okay.

The Admin: So we gradient clip equal to one. So we do not accept more than one gradient has nothing to do with what we're discussing. You're not talking about the amplitude and today we're talking about the direction you realize 999 is trying to reduce the changes in the V.

Swati Bansal: So the 999 is trying to reduce the amplitude only. Yeah. Yeah.

The Admin: This is always positive It's all there is the gradient that we just calculate for the loss.

Swati Bansal: So there's no direction. Okay. Okay.

Dattatreya Manjunath: U so g square if it's just a derivative of v or new right right how is it calculated for sorry of gradient right or…

Dattatreya Manjunath: is it just gradient Okay.

The Admin: Just gradient square.

The Admin: We can't calculate It's just gradient square.

Dattatreya Manjunath: No, because you said thousands of values. That's why I was just trying to so gradient usually is just one value that you kind of look at.

The Admin: V 999th version and…

Dattatreya Manjunath: How does it work with thousands of values? okay.

The Admin: V,000 version that's all I'm saying. I have calculated this equation times earlier. So we have V mu is equals to 0.999 V4 \+ 1 01 into G².

The Admin: You clear? I want to talk to you. Say yes.

Dattatreya Manjunath: Yes.

The Admin: Let us say the gradients are something like this. Some weird value, but I'm keeping it my life easy. Clear. Okay.

Dattatreya Manjunath: Yep.

The Admin: And Let's say thousand times I'm on this scale here. That means the V 0 would have been 0.001 here.

### 01:15:00

Dattatreya Manjunath: Right. Yep.

The Admin: So V new is equals 999 into 10 \- 3\. Okay. Plus 0.0

The Admin: 0 0 1 into G square. suddenly G happens to be let's say 1 big number compared to what we were earlier at the G square is also one. So I'm going to multiply it with one. So look at the effect of change of this guy. We are saying that we want to rely more on our past compared to the new effect that is coming in. So new effect has to be thousand times bigger just to cost 10% change in this. Not even 10% somewhere around that.

Dattatreya Manjunath: Got it.

The Admin: Is this part clear they will neutralize each other. Now it will develop. Right? So I'm writing N and O here. But this is literally the thousand step and this is the How much the new step gets affected by the sudden change in the gradient? That is what we're trying to compensate here. Okay.

The Admin: Simpler way would have been to just say that our na is equals to 1 by 1x g here and then we are multiplying by g directly or g square here right I could do this v n is equ= to v 0 plus and…

Dattatreya Manjunath: Yeah. Hey.

The Admin: we have beta 2 or we have 1 minus beta\_2 and then we have g square here correct slowly we are getting this term built up v 0 starts with zero correct So slowly g square g square is telling us the amplitude that I'm interested in right and…

Dattatreya Manjunath: Yeah. Hey,…

The Admin: let's say this is a 0 and one scale. So this is one and this is zero and these are the steps that are coming in.

The Admin: So let us say my G was something like So my G square is going to be something like this. First of all it's a positive value. Correct. Right.

Dattatreya Manjunath: thank you.

The Admin: This is G square coming in. Thousand times I've accumulated That means this is my current V. Correct. Now suddenly…

Dattatreya Manjunath: Got it. Yeah.

The Admin: if we have a change in G which let's say goes here it's not going to affect me a lot because That's all this equation is trying to do. Okay.

NITIN YADAV: So just a confirmation you are talking about on later state but in the initial step does this allow the learning to be Slow.

NITIN YADAV: because we are taking the history a lot not the current point.

The Admin: That's correct.

The Admin: There is no other solution.

NITIN YADAV: Is it somehow?

The Admin: And those initial steps are literally thousand steps.

NITIN YADAV: Okay.

The Admin: So maybe 1% of the whole training schedule.

NITIN YADAV: And is it somehow being compensated when we update the weight this new is getting EA by new. So there we are considering like that.

The Admin: What is the question?

NITIN YADAV: Okay. Sorry. Ignore that. Yeah.

The Admin: Correct. Automatically

Mukund singh: Hi Ron. So for parameters which don't get updates very frequently for which we have shorter history. This still will give higher priority to the current update right the current stage. Yeah.

The Admin: So Adam takes both of them. Adam combines the two averages, right? So the first one sets the direction of the step which is going to allow us something like momentum and the second sets the scale. So Adam literally takes the per parameter learning update where we have this one minus one divide by new term and it takes the momentum also in consideration. take momentum and then you take per parameter update and what you get is Adam. That's literally it, right? And the equation is Looks very complicated, but it essentially allows us to take both the things into control. What is Momentum allows us to not go left to right. A lot of times it takes sort of a vector in the direction. And nita, we saw the new we saw is per parameter. So you mix both the terms, then you get as a parameter that allows us to scale the learning rate for every single parameter.

The Admin: Then we add momentum also to make sure that it actually is consistently going in one direction. That's why atom works the way it does. And every single time you see you're going to get a similar kind of update for the overall bit you're seeing is very close to one here right and if I remove the bias correction if you do not do the bias correction that Adam does which is that divide by thing essentially off. We get very very big bias correction make sure that every parameter gets exactly the same kind of update with it own relation right so if I'm talking about 0.01

### 01:20:00

The Admin: 01 it gets update to its scale. If I'm talking about a parameter initializer 3, it gets a weight update to its scale. That is all we're trying to show here. That is what this vhat does. Are we clear on this? Adam is a combination of momentum and the perimeter update that we want, right? It doesn't matter how much gradient you push. Adam will make sure that all of them have sort of here you see gradient 5 \-4 04 55 but Adam will still make sure that every time it is still in the positive side still in the direction if you don't do the bias correction you'll see that it's weird any question on this complete rule sort of becomes this W into NA momentum term / new that we looked at and epsylon is

The Admin: the 10 \- 8 term. We just want to make sure that this is not zero. Initially the model can be zero or some weird calculation can happen. So we don't want anything divide by zero. So we just add a very small term to make sure that the thing never goes to mathematically heavy but you have to go through this questions please I want you to see

The Admin: The last complicated topic that we need to discuss is the weight decay. what happens is weight tend to grow over long period of time and large weight makes the model brittle. I hope you remember the first couple of session I mentioned that we want all of our weights to be between plus one and minus one right and if that is there then we know that it will always be between that because if I multiply let's say 0.999 even 100,000 times or 10,000 times it is still going to be something that remains on the plus and minus one. So everything is contained there but you can't guarantee it right because we do not have a term for making that sure.

The Admin: So the remedy to solve such a problem or the problem is that the weights might become big. Let's say the weight might become 10 or 400 or 4,000 or 4 million. We don't want that to happen. We add a term weight decay is a kind of L2 essentially means you take a square of it. Regularization something means that allows the model to go to its minima in a faster rate. Regularization also means that it is invariant to some noise that is coming So there are many ways we can understand Regularization is a term that is very easy to understand in case of convolution networks. But here what you need to understand is it regularizes the weight. It regularizes the model to be efficient. And what is the problem We're trying to solve a problem where our weights become big. So how do we solve that? This is our loss term where that you should be aware of. This is a old loss that

The Admin: aware of the square loss or we want to predict 0.00001 we are predicting 0.2 0.001 0 0 1 0 02 and then we are predicting 0.2 I've taken so 07 0 something right so negative of all of this square of all that and add all that right so whatever this value comes in is a loss the same thing that we saw earlier but when we add one more term which is half into lambda a constant generally again 0.01 but need to be fine tuned between this 0.0

The Admin: 01 What is W square? So it's written as a simple way here assuming that we had only one weight. But this W square is actually summation of all the weights and the square of that. So let's say our model has 1 billion parameters. We're going to take every parameter so W1 billion parameter take a square of all of them and add them. And that is a huge term. We add that to the loss. That's why Lambda needs to scale it down. So this is one of my favorite topic. And the reason it's favorite is because it's actually a very good concept. who do I want to talk to? AJ, you have not spoken today. You there?

### 01:25:00

AJ Jain: Yeah. Y happy me.

The Admin: Okay, Can you imagine this is you?

AJ Jain: Y I haven't figured the answer for that question.

The Admin: Okay, you want to work I'm giving you a scenario. You want to work in your own company or a startup or something where that you're going to be successful have a amazing career and so on and so on and earn a lot of money but you need to spend 24/7 there right to actually crack it. here is your love where that if you spend more time and you have to go to mall and spend time and spend money and other stuff but you're doing all of this for her only. How will you balance your life? I should give you the answer but what will you do?

Manjith Adapa: Make this company.

The Admin: We need some sort of balance here right you're going to say okay not 24/7 maybe 16 by five and rest here something like that right so what happens in neural networks is if you say the loss L is equals to L1 \+ L2 is a very beautiful concept if we make a loss as a combination of two losses they start balancing out themselves which also means that…

AJ Jain: Okay.

The Admin: if L1 was let's say 11.2 2 and if L2 was 10,000 model will focus on

The Admin: only this clear. So we need to add a term like lambda which is 1 /,000 to make both of these combined losses similar to each other. Then we can say we have a balance and that is exactly what this loss is doing. That is exactly what this lambda is doing. That lambda here is that balance for us. So we have to figure out what this lambda is. But if we can figure out a good lambda then what are we saying? We're saying that we do not want the amplitude of all the squares of all the parameters to be very big and we also want to solve the loss which is activating the next token. So now the model actually tries to only affect those W that are not going to affect What if it starts changing that has a big effect on L? It can't.

AJ Jain: Yeah. Mhm.

The Admin: So we will now only start targeting those W's that are going out of the hand which can be cut out like your night outs with your friends for whole night drinking and stuff you're going to stop doing all of that stuff. So suddenly the balance is going to be that moment you have a kid you have a balance in life right suddenly all the activities stop but you still go to your job and it's not the career stops after a kid. So that is what this combination of L1 plus L2 does to neural network also. So if you add more terms here it will try and balance all but the balance is going to be based on the amplitude of those effects. So lambda becomes very important for us. So if you can figure out lambda for every new loss term that you add it's going to behave magically Another example imagine that we are making an image so it's coming from I forgot let's say then Netflix is trying to create an image.

The Admin: And it's not even create image.

AJ Jain: Mhm.

The Admin: There's a new network that is trying to make an image which is similar to this image. there used to be transfer concepts earlier. We're doing a style transfer, right? So you might have seen applications where you have a Picasso painting and you want your painting to be made Picasso. Yes. So the loss is very simple. how similar your image is to Picasso image and how similar is the new image with your image. So if you take this and solve it, you get your image as if it's designed by Picasso. And again the terms here lambda 1 and lambda 2 affect how much you want it similar to be your image and how much similar you want to be Picasso. So if we can balance L1 and L2 lambda 1 lambda 2 we get again this file transfer. another concept and…

AJ Jain: Oops.

The Admin: this is coming from YOLO one of the best object detector.

The Admin: In it loss function we have so what yo does is it predicts something like I'm making up these numbers so don't quote me 100k prediction bonding boxes right so for an image it is going to be predicting 100k bonding boxes clear yeah that I think there's image for every single area, it says that I think image object might be here. if the loss was u and let's say this is If the loss was correct bonding box loss, Model needs to be trained on two things. Correct bonding plus wrong bonding box prediction. The model has to say that yes, this box is there. I'm confident a box is there.

### 01:30:00

The Admin: Fair enough. But it also has to say that I'm confident that the object is not in these boxes, Again, to keep things simple, let's say yolo was predicting five bonding boxes per image. There's an image and it's predicting five and this five comes from how many objects it can predict. that used to train model like that. There's a capacity on how many bonding boxes the yellow or any algorithm must predict. So we have bounding box 1 2 3 4 5\. If the loss was that okay this is the correct bonding box and yolo has predicted correctly it starts predicting something here also and we have never trained it not to.

The Admin: So we have to train YOLO to predict that you have to predict the bonding box is here and…

AJ Jain: Yeah. Mhm.

The Admin: you also have to say these bonding boxes do not have objects clear on this AJ okay but the problem is we are asking yes once and we're asking no four times correct so if you just add these two losses it just starts learning no for everything because it still gets 80% correct. Hence, we have to divide this by four. So, we have to figure out that lambda, And that's the beautiful part that if you can figure out a loss function that is a combination of many losses, we're trying to optimize the equation at many different way. For example, if I train a neural network and we say that the answer always has to be in Hindi. So, not only has to predict the token also has to be of a particular kind. That's a scientific or shashurian complex words.

The Admin: then you're essentially training it for a specific use case. But we need to make sure that the lambda is taken care of both of them. Van your voice is cracking a lot.

Vardhan Walavalkar: So I'm not afraid of this.

The Admin: Your voice is cracking a lot. Still can't hear you.

AJ Jain: So this is very applicable for our thing because out of 13 1 072 we have to identify the next token.

The Admin: Correct that cross entrop is taking care already…

AJ Jain: So it's also training on the negative the ones which we have to okay.

The Admin: but that's one kind of loss right we are saying another kind of loss let's say we add one more loss to it then how to optimize for that we need to have this lambda term okay so essentially does that

The Admin: What this is trying to show you is let's say we have a parameter of as okay so if we don't do that one divide by a new term or don't do that u parameter update then we have a decouple but for that particular okay I need to explain the atom w side now v is fine vk works alone very well we can just add this lambda term it works well but when we add with Adam not Adamw when we add with

The Admin: the decoupling happens. What this means is that because we are also trying to reduce a particular weight, the atom weights go haywire because atom weight was designed for a particular weight now this weight update is trying to reduce that parameter itself. Right? So we get a decoupled kind of situation where L1 and L2 both becomes very weird and that's why we need to make sure that we have another term in Adam that fixes that particular issue right and those terms need to be can be calculated directly by AdamW. So what are we saying?

The Admin: We are saying that again what have we covered today we discussed that a simple W new is equals to W old minus beta into gradient right but the problem here is that okay and from here we also realize that based on the learning rate either our next update is going to be 0.98 times of the

The Admin: last update or distance that we get So 10 kilome 9.8 and so if this was 0.01 but if this was a big number then this will fluctuate a lot. So meter cannot be big. Ma has to be small. Then what we discuss is that even after it's small it's still going to do something like this. To contain something like this we introduce momentum that is going to allow us to actually average out. and this term doesn't happen. We take the second term and literally go from there to there. Momentum. So this is the momentum thing for us. Then we discussed that there can be a scenario where we have two parameters one coming from this side to this side right or if we had a hill for example right just imagine that we have a hill here and then we had a plane here and this is where the loss is.

### 01:35:00

The Admin: So one par parameter is initialized there. This can reach faster. This is going to take a long term to go there. Same thing is happening here. In that case that we discussed that we need to have different learning rate for different one. And the simple rule is that we divide by the history of the gradient update itself. The square of the gradient So we have momentum and then we have one by mu. So we can take both of them and that becomes Adam for us. That's what we discussed till Then we discuss What is weight decay? sometimes parameters are not like this. Sometimes they become this and they really add no value. Bigger amplitude doesn't do anything much in neural networks. So we add loss plus lambda into A weight square is basically this

The Admin: itself but we don't have one weight we have millions of weights that's why this lambda is also required to make sure the overall loss we're adding because of big weight amplitude is not much so the size and balances out but the problem is that in Adam we were doing two things we were maintaining the momentum of a particular weight and then we were also maintaining how small that weight was and updating the new for it now because this term is changing w itself is not really compatible with Adam that's why Adam W came in and Adam W solved it using these square V terms. Right? So now Adam V is slightly different. The new term is going to look something like W minus ma is the fixed learning rate.

The Admin: have m the momentum thing new plus epsylon which is the I'm forgetting term what do we call it there per parameter learning rate from there the new is coming in minus we have nita and lambda w right so our weight decay also becomes the part of it so the equation balance And then this is what this is trying to show essentially that we add that term also into the atom to basically tell atom that we have L2 also and then it becomes easier to handle. Are we clear on this? This is as complicated as it get what I covered in last probably one and a half hour should take around 20 to 30 days of manual coverage from your side to be able to get to the point where we are.

The Admin: So I know it's fast but you still need to know a bit of background. What you need to know from practical term is that we can't use Adam anymore. we have to use RMW if you're The good part in all of this is that we might not be able to use weight decay. So we might not want to use Adamw. So we're going to discuss that when we discuss our own architecture. let's talk about the optimizer memory cost. So we've discussed Adam, W and so on. So the weight in B16 is going to take us two bytes. The gradient B16 is going to take two bytes further for that. The full precision copy F32 is going to take four. We need to have a full precision copy because all mathematics happen in full precision. We do not because when we multiply two things and we're calculating something, we want that to be as much precision as possible. These numbers are small. We can store them in a B16, but the calculation should happen in FP32.

The Admin: The gradient average is also going to take four bytes because the square gradient average should also happen in FP32 that also take four. So for a single parameter we end up saving 16 bytes not two bytes if you're using Adam So that's where it becomes expensive. That means that for gradient descent simple I need 67 Moment we add momentum to it, we take 100 GB of Moment we add ADMW, we go to 134 GB of memory. And we take 8 bit AdamW. That's sort of a compromise that takes us to 83\. So we need to see which one we want to take. So it's a big hit on the overall computation budget that we have. So same thing is shown here. Grad is simple. Momentum Add W adds more.

The Admin: 8 bit item takes a slow and depending on how big the model is our RAM requirement are going to go haywire. So we need to be careful on which fun we pick. Gradient descent with momentum rule out they don't work for LM AdamW is option for us. So Adam add 8 bit Adam is also an option for us but there is accuracy disadvantage with 8 bits. then learning at warmup. initially we have an that is coming in but the problem is it's very noisy.

The Admin: Initially everything is extremely noisy on because we just randomly initialize our parameters, So we cannot have the maximum learning rate we want our atom to go to from scratch. So our policy is going to be something of this side. Now you see this line that is the actual learning rate that we are following. But it's a mix of a lot of different things. I want you to see what is changing right now. Do you see this ramp up changing this first curve changing? Yes or no? Okay, this is a Ramp off. We decide what the learning rate should be and we slowly anneal it to a smaller value. But we have to have a ramp on where we start from a very low value then hit our main value and then do some sort of cosine decay or some decay to better understand. Let me draw it myself and then we going to look at we have Adam and all and everything else that is internal to the model.

### 01:40:00

The Admin: We are not aware of it. What we supply is a starting learning rate and the ear end learning rate. Are we clear on this? you can speak up?

Avnish Midha: Yeah. Yeah.

The Admin: So we have a starting learning rate and ending learning rate. So now simplest model we say learning rate is 0.001. Okay. Okay.

Avnish Midha: Okay.

The Admin: So for number one to step number 1 billion this doesn't Fair enough. But problem is as we discussed earlier we had a weight of 0.02396 and it had to become 0.2395. This small delta cannot happen here. So generally what we tend to do this…

The Admin: if I draw is a constant learning rate.

The Admin: Generally what we tend to do we have a constant learning rate and then we say that we are decaying a learning rate to a small value. this allows us to so this is strategy two where we have a constant followed by an analing which is going to a smaller value. Okay so we have a constant going down and going down is possible in any ways we can do straight and cosine decay which looks like this. Okay, we can do a straight line also,…

Avnish Midha: Yeah.

Avnish Midha: Okay. Yeah.

The Admin: So we have either cosine or we have straight line. So two methods for that.

The Admin: Then we saying that we don't want to start directly at a height. We want to start from a small learning rate reach that high maintain it properly or then we do want to do cosine decay. Say okay. So this is called ramp up this constant phase and…

Avnish Midha: Yeah. Yeah.

Avnish Midha: Okay. Yeah. Yeah.

The Admin: this is called cosine elite and yeah sometimes we don't say that we want this at all.

The Admin: So we just do this and let the cosine decay takes it on course because we can just make our cosine decay longer. We can just say that it's like this say okay right and that is exactly what is shown here. That brings me to showing you guys something. I'm not sure someone shared an amazing link. not sure how many of you are following it. I have lost the link. no, I have not. Okay. Someone shared this amazing link in the group. here's a team that is actually training the model live as we speak and you don't have this link then let me share it with you. Right.

The Admin: So these guys are training their own model right now. And here you can actually see the learning rate they're following. Right now they're in the learning rate. You can see how the gradients actually behave. This is a big model by the way. I think some 300 400 billion parameter model. These are optimized stage but these are recent stages. Do we have old stage? Yes, this is slightly older. this is dropping but it's still advanced stage only. Okay. What I'm not able to show you is you can see gradients here always less than one. some of the parameters they are following parameter per norm and so. We need to make a table like this. We were also following our training like this.

The Admin: I'm seeing if we have the learning rate somewhere. No, We have a Train router on the system side. GPS. No, we don't want that. We want No learning rate. Do you see? We are in the fall stage. They're in the end stage. So if you go look at all of these runs, maybe you can find out some initial run where it started with a big loss and then it's stopping. This is fourth September already. Just have to see how many experiments they're doing right now.

### 01:45:00

The Admin: latest. Okay, I'll try and find the actual one. This is the latest one so we can see how they progressed through. But it's very good idea of what we are also going to be doing and following up.

Dattatreya Manjunath: Since we…

Dattatreya Manjunath: since we only learn after a pretty big chunk or a B size. is warming up the learning rate still useful?

The Admin: 200%. It's a very short period.

The Admin: Here I'm showing a very big period but it's a very short period. So this part is cosine kneeling essentially and for initial few steps we have slow incline and that is literally because initially as all of you are also seeing you see the equation one step and see everything is noisy so we need to collect some initial information before we hit the proper run. So this analing the initial state is required right just to balance or…

Dattatreya Manjunath: Hello.

The Admin: just to get the model in a stable state.

The Admin: So overall we have learning rate schedules. We have a warm up somewhere around 2% of the overall. Then we have a stable flat or maybe a cosine kind. And then we have a final analing stage which is this part. And you'll not believe most of the learning happens here. And I can actually show you I love versus loss.

The Admin: This is a good example. You see the red coming down here and please remember that from going from five to let's say two might look much bigger but nothing is happening there. the model reaches a good stage only after we are at these kind of levels right and there a movement from point 1.1 to 1 05 is a big change that is where the state-of-the-art made it's very fast you can see that everyone here reaches from 2 to one it's very very

Dattatreya Manjunath: So if the initial learning rate is very small reaching from five to two in itself wouldn't it become slower and…

The Admin: First everyone use Yeah.

Dattatreya Manjunath: they are using that ramp up ative market.

The Admin: Everyone uses You can see ramp up and drops fast, right? And after that it takes a lot of time. Every single curve is going to be like No exception. All right. So we have a schedule that we have to figure out. when do we want to stop is a question for us. So this is money for us. then how much run is expected Plan run length that is something that is important for us. Then we also have to figure out that we are going to follow which policy.

The Admin: So we have three ways of handling our overall training. We have constant not going to do it. We have WSD is very interesting and we may actually run part of the model in WSD and then we have cosine. Coine is simplest one. Nob WSD is risky but the rewards are very very high. Let's say what is WSD LR. So this is WSD which says that do the initial part then keep the learning rate constant for very very long right and then suddenly drop it. the reason this is risky is because not seeing the loss drop is very nervous being you feel very nervous right you have to commit to the fact that for the 90% of training you're going to keep the loss at a fixed rate let's say 0.1 at a fixed rate and your loss is not going to

### 01:50:00

The Admin: drop compared to others. For example, here let me compare it with some other so I can share my nervousness with this is how nervous we have to be. So we have to commit that are we okay to handle something like this?

The Admin: This is what we're discussing the L square cool down or u the cosine thing that we're discussing, So we have this ramp up and then we have something like this. This is the graph that we get and then we have this In WSD we go straight, we keep it constant and then we sudden drop. Now WSD has been proven to beat the cosign nearly in every single paper that is out there. But it's so damn risky that you see that the blue where it is better than green, But it's very risky. So I'll not be ashamed of saying I do not have guts to do WST but all Chinese are doing WSD. can you feel the emotion here? What is it that I'm trying to explain?

The Admin: Yeah, this is a really really good example of what I'm trying to tell Open imaging. So the question to you is do you have guts to do WST look less tokens and we reach that particular loss point here compared to cosine which takes forever. We can reduce the training time by half. question on another problem is that we have to figure out when do we do the drop?

AJ Jain: What's the intuition behind this?

The Admin: This is fine, but when do we actually do the drop? Somehow we have to figure it out. AJ Yeah.

AJ Jain: Why will keeping it constant suddenly dropping will it be better than cosine or

The Admin: So there's a story and it can only be understood from that gy. There are two analogy that I want you to understand. The first analogy is the story of a farmer. yeah. Theres Looks like a farmer. Okay, there's another farmer. Okay, this guy has a car or a truck. This guy also has a truck. Now, both of them are farming potatoes. This guy takes all the potato, put it inside a truck. This guy also takes all the potato, put it inside a truck.

The Admin: This This guy takes the baddest road possible to the market. This guy gets $100 for his work. This guy gets $200 for his work. Can you tell me why? Have you heard this story?

AJ Jain: No.

The Admin: Anyone? So when this guy takes the best road to the market the way in which he packed the potatoes remains there that doesn't move but because he took the worst possible road in his truck what happens is the smallest one drop down bigger ones are on top and much bigger on top. So you can actually sell based on the size that they have and there's a big requirement for buying bigger potato compared to a smaller potato.

### 01:55:00

The Admin: This guy can't guarantee that. Just a small process change here has allowed him to filter the potatoes that are held everywhere. Is this clear? So a lot of shuffling is happening in his truck. second intuition. This is a minima and then we have this This minima let's say gives us a loss of 0.96. This gives us a loss of 0 999\. So this is a bad loss compared to a better loss here. Right? 96 compared to 99\. So this is a higher value or 9\. We clear on Which model do you want? You want a model which does this?

chirag Tagadiya: Second one.

The Admin: Why second one? Intuition is telling a second one. But why second one?

chirag Tagadiya: Yeah, because there is a lot of rooms to change if you want to change in future.

The Admin: Exactly. What is happening is here if your car was red, if your car was seen from the front, if the image was very clear, if the tire was very clear, then it's going to come back and say it's Maruti Swift. Here we have white Maru Swift, then green, dirty, and all. So it gives you a lot of room for being able to correctly predict something. So we want our loss values to be As wide as possible. and then there's a guarantee that you're going to get a good loss. Now if you mix both of them what is happening is if this is a parameter and you keep the learning rate constant for very long it

The Admin: shuffers a lot right it's a big LR that we have asked to go for it compared to big and small and then slow reducing this is a cosine this is WST so when these parameters are oscillating for so long all of them end up finding this value and all the parameters find a deep value where the performance is really good that's the only induction I can provide why WSD works compared to cosine every single parameter they kept at such a high isolation for such a long time that they end or end up finding the biggest values possible and they settle down there and of course in the WSD we also have the slow end step this step make sense that take

Dattatreya Manjunath: So Ron you said that there's a lot of papers and almost every paper it's usually using WS right is there any insight on…

Dattatreya Manjunath: how they're mitigating the risk for s we can learn now or…

The Admin: You can see they test multiple times.

The Admin: We have WSD at 40 and 2N 60 and 2N. Yeah,…

Dattatreya Manjunath: just play around with that And the next thing is …

The Admin: play around with that. You have to figure out this somehow and…

Dattatreya Manjunath: what if during the end stage we basically train on the same data with same learning rate and…

Dattatreya Manjunath: by sharply reducing the learning rate. Wouldn't that help a certain sense?

The Admin: I didn't get the question.

Dattatreya Manjunath: So just that we train on some super curated data with the constant learning rate at the very end and…

The Admin: No, no change. No, this exactly same. The data doesn't change here.

The Admin: We are not even talking about moving from one station to another. This is still the training right every time you see this paper you would have seen that they are just breaking cosine left right and…

Dattatreya Manjunath: it's in pre-training only. Okay.

The Admin: center but I think if I train four five times and then confidence will come in very risky. So we need to figure out can we do the batch size and the learning rate. before I do that I wanted to see this widget here. We have a batch of 56\. Let me reduce it to eight. We have a batch of eight. So 1 2 3 4 5 6 7 eight dots are there. Right now in eight dots we are getting noise from noise or information from eight. Right? And we're taking average of that and then we updating a parameter.

The Admin: Are we clear on this? In a batch of eight, we have eight samples. From there, we are calculating our loss and we updating our gradient that we have. Yes or no? as I increase the batch size, you're going to see that I get more samples to calculate my loss form. And as I continue to increase, you're going to see that finally I'm actually approaching the point where I may be getting a true gradient. The global batch size has to be big as big as possible. But we have a limit of How much we can put in the GPU together.

### 02:00:00

The Admin: And that's where the thing comes in that we can do grid inclination. So if you do grid inclination and we change the batch size then we should be able to get somewhere we want. But you should also see that a big batch size does allow us to go to the true gradient. And the smaller one has a smaller amplitude also. So there should be a way of sort of adjusting the smaller badge gradient multiply with something that takes us to something like this. you understand the hack I'm talking about. There should be a way of essentially matching these two right and that is what this section is all about.

The Admin: When we have a eight for example batch size and let's say we have the gradient coming in as one as we increase our batch size we are changing the effect of these samples we're changing how many of these actually affect the overall loss that we have right which means that we have a relationship especially in case of Adam where we have a relationship of twice if the global bats this is a different table first look at this table let's say we acclimating four times this means our learning rate is four times but in case of Adam it's the relationship of square root two. So if we were training our model at a batch of 8 and we had a learning rate of 0 I can write it down so you will also remember it. If let's say any batch size right so we are saying let's say the batch size 56 if my learning rate was six not six what am I saying 0.01 or 0.001

The Admin: If my learning rate was 0.001 for a batch of 56 and I'm using now an accumulation of four. So I'm waiting four Learning rate in Adam is going to be two times which is square root of this. Are we clear on this? This is what this table is trying to tell Yes or no? We're training a model. Suddenly you decide okay let's do gradient information how does the LR has to be square root of the change in the batch size now let us say we increase our GPUs to 32 so we can go 4x from this right again we have to do 2x of LR not 4x and if you do both of them together then the effect of 16x so we need to take a square root of 16x and that is the 4x for the LR right so we can increase the learning grip by four times if

The Admin: increase the GPU by four times and do great incrementation of four times. Okay, this is what this table is trying to tell you. You need to know the solution because when you're training and this will happen to us. We are training at a 4K. We figure out batch size everything and then we want to say okay let's change for A longer sequence. We have to buy more GPUs. We can't do gradient information done. We forget the changing change in LR. We need to remember that if we are doing the gradient information then the LR has to change. Are we clear on this?

The Admin: Many of these are by the way values that come from research papers. So you can't say why that. These are the empirical that is…

Avnish Midha: Yeah on one question I believe then if the batch size is higher we can increase the learning rate right and…

The Admin: what we're saying if that is similar to gradient accumulation.

Avnish Midha: secondly okay right yeah and…

The Admin: So if our batch size goes by four our learning rate can go by two.

Avnish Midha: suppose if we were to train on five different types of data or…

Avnish Midha: 10 different types of data do we create a mixture of those in each batch or is it Take only one type.

The Admin: that comes from…

The Admin: what for us is one type it comes from in the curriculum we can have different weights for different examples or different topics but is same for all of them we don't say that we train on Sanskrit at 1.2

The Admin: 2 and we train on Hindi English at 0.2. We don't do that.

Avnish Midha: But what if we mix the data in such a way that every batch has a mix of all types and then we take an average and maybe have a better learning rate or something. I'm just wondering.

The Admin: That is what we do already.

Avnish Midha: We already do.

The Admin: That is the default state.

Avnish Midha: 

Avnish Midha: Okay, cool. Okay.

The Admin: This is a very interesting concept, extremely new. this is called mu p which is maximal I forgot it one second maximum there's something in between also

### 02:05:00

AJ Jain: on one of the other links it mentioned update in the previous this one. Yeah.

The Admin: maximal update parameterization.

The Admin: That's the full meaning of it's a paper and we're just looking at the results of the paper. What happens is how do we actually train a model and this is super important from our point of view because everyone else does it we also need to do it and that is going to give us a really really good idea. let's say we decide finally that we're going to train a 27 billion parameter model. that's not the first model we're going to try and train

The Admin: we might train let's say a 1 billion parameter model there are two ways in which the future can lead us to one is that we grow this model in 27B and that is what we did in V4 and even in growing we have to figure out LRs and other things and the other is that we learn the hyper parameters then train a bigger one 7B and then learn from it and then train a new one on 27 right two ways so either we grow or we take the learning from this and then every time we are training from scratch So one cratch 27B strain from scratch. Other strategy one B we use these weights in initialize a bigger one and we train and we use that initialize the bigger one and we train and we do that right this is the second step is what we followed but that's not the point point is because what I'm going to discuss is applicable in both the cases. So we train a 1 billion parameter model because finally let's say we want to train a 27B model.

The Admin: Here we going to figure out all the things that we just discussed today we have hyperparameters we have u WSD schedule and many things that we have to figure out this new paper actually said that there is a relationship between this and this guy and those relationships are actually simple what it's saying is that if you're going to change the width how do we increase the model very simple let's say I'm sure someone would have calculated okay

The Admin: Yeah, I can use that. So, we are seeing parameters in billion by per parameter. But that also is tricky. Okay, let's keep it simple. Let us assume that we have 256 dimensions, right?

The Admin: So 256 dimension what is the first thing that happens? We take that we do KQV. So we have getting into three different neural networks. So we have into And then this gives us 256 back and then we do a four times increase on top of 256 and then we collapse Fair enough. So we have into 256\. That's a collapse that we get, And that's a per layer parameter that we have. I'm doing a absolute simple calculation. I want to take out. 256 I want to take 256 out which means I have it twice. to 56\.

The Admin: So inside I will be left with \+ 4 \+ 4\. Can you see that? into 3 \+ 4 \+ 4\. So 11 is inside right. And I can simplify this further based on the dimension I have. which is going to be 256 raised to power 2 into Clear something like this. this is what 256 is. if it's not 256 but 512 so our 720,000 parameter are going to become 2.8 million parameters right and this is how we increase the model so we make it wider so all we have to do is to make 1B model to a 3B model or a 4B model is to just go inside change 256 to 512 another way of doing it is to actually add more layers so here we're only talking about width when we're going to increase the width of the model that we have.

The Admin: So can become 1024 and 4028 and 4096\. We're going to do both. We're going to increase the width and next step we're going to increase the depth also. Here we're only focusing on increasing the width. So what this says is that if you turn the MU on which is the calculation for MU this is the kind of graphs that you're going to get different learning grades. But if you keep the MP on while training, we can actually get a graph like All calculations on all whatever we have to do, we're going to discuss everything later on. But the logic is that if you keep the MOP on, which is a calculation of how we do, it's a process that we need to follow. If we keep the map on for all the models as we are fine-tuning them as we are finding parameters for them we can get a curve that looks like this compared to very hire haywire where we can't figure out what is happening. Are we clear on this? So learning rate transfer can happen.

### 02:10:00

The Admin: So when we train our model we follow the MVP process where we will track the parameters in the way it describes and using that we can make a model go deeper and as we go deeper we'll be confident of whats at the same learning rate we can go deeper essentially that's the point clear yes or no AJ you got Okay,…

AJ Jain: Yep.

The Admin: it's a strategy we have to follow essentially. Okay, we had AdamW, we had all of the other stuff. Then came Meon and Meon and Meon Clip and Happy Ball. These are newer optimizers, but essentially they are faster, right? And China is really on top of it to make sure that they work really really well.

The Admin: they have worked on the matrix level of where the multiplication happens for these parameters and optimize that. that's the max thing that we need to know about them. So, MON replaces the atom because they've done optimization on how it's calculated and there's a singular value decomposition that we're going to discuss later it basically means is that if I have 100 cross 100 matrix and it is about to multiply with 100 cross 100 matrix final output is 100 right so 100 cross 100 100 goes okay this is similar so let me do 120 cross 100 and 100 cross 120 right so if I multiply these two I'm going to

The Admin: get 12 cross 120\. But I can do something like this. 120 cross if I do this, then it's going to give me 120 \+ 10\. And I can do similarly for the other side. 10 \+ 100 and 100 cross 120 and that will give me 10 cross 120\. And then I multiply these two to get 120 cross 120\. So if I can find out this kind of matrix which allows me to make my bigger matrix smaller then the actual calculations are going to be very small. Right? This is the actual calculation that will be required. So this concept is going to come out when we discuss LORA and other things. So it's very similar to that concept allows RAM overall reduction in total tokens that are also required to process because it focuses on the values that are changing more. We can go deeper than what I just discussed.

The Admin: I just wanted to mention that now we have a new optimizer also. Hyperball just came in reports 20 to 30% over AdamW but the scale is 1.2. So we need to think of it deep So lot that we discussed today but question now is for us to figure out Adamw or meon. As I said weight decay may not be possible for us. We need to discuss why that later on but we need to figure out are we going the Adam way or the mon way. Second is whether we're going to spend a day on a MUP sweep at which 256 to 1024\. We have to calculate for all of them at the same time. So one full day of processing required it's going to cost but it's going to get a really good value really good understanding of whether the training is going or not. another question is that one learning rate or a separate head for the output head is another interesting question. Should we have a separate learning rate for the MTP that we might add because some people are doing it some people are not doing it.

The Admin: So labs are doing it. So we need to be careful whether we want to do it or not. And whether to decay the chronical factors in session seven. So we have chronical factors. Do we want to decay those also or we are okay with the chroner layer acting normally. So there's some other question that we need to take from this and of course we're going to add our chroner encoder and decoder that reduces the overall burden that we have. But main question is essentially which one are we going to use? So you can use RMW or muon. I don't know when talks about it or not. When

The Admin: They're using both now really the mon optimizer used refined around orthogonalization accuracy the division of labor between muon andw and splitting the fuse parameters with a scaling law of new architecture they have used both…

### 02:15:00

AJ Jain: That's a good

The Admin: but you can see that most of them go actually on

The Admin: Muon side really you're going to find that muon is not used by a Chinese model they're always muon and openai and gemini and others have stopped publishing their report so we actually do not know what they are using today you have to read it this 38 paper just came in so I'll also

Dattatreya Manjunath: How do they distribute between using at different stages they're using different optimizers not at the same time All right.

The Admin: I have to read it. Different stages. Difference. No, we don't do that. We never do that. You do not train on Adam W and suddenly move to Mon. Remember, we have train on 40 billion parameters during Adam. We have that history. We can't delete it and suddenly move to Mon. So here we are saying the division labor between Mon and AdamW and the splitting of fuse parameters and scaling law. So they would have figured out some layers that are okay for me on some layers that are okay for the R\&W and proceed with that. I think they would have gone for the head with something else. Head is where the difference might be. I do not know what is PSO questions before I introduce assignment. I know today's a boring session.

The Admin: a lot of math but there is no other way to go through this once you have to go through this and tell yourself that there are things either you fall in love with this or you just say that okay I'm okay to know whatever I have and I want to proceed that's where I've kept myself in I do read about these things in as detail as possible but finally I realize that is this the thing that I need to know the max about or there's something else that is there so that's where I essentially decide what do I want to learn what do I don't want to Adam has spent a lot of time because that's one that has been sticking for continuously a long time. So the assignment for you and your claude is to ask your claude to reproduce Adam by hand. Take one weight and five gradients and compute mu cap and vcap yourself and the resulting yourself. You can check again pythos if you want basically right.

The Admin: So you and your cloud are going to now take a weight and add the five gradients and then compute V. V, Mu, Muhat and Vhat and then write a small Python script to test again. If you do not have Python installed on a computer, you can just use Google Collab. Now disable the bias correction as we discuss. We have not discussed the bias correction but I wanted to figure out Bias correction is what AdamW is doing. We discussed it AdamW doing to make sure that it is not getting affected by the weight decay. Right? So that is the bias correction. So plot the first 20 steps.

The Admin: Then log the weight to update ratio for every layer and identify the step in which the warm-up starts actually changing it. train the same model twice for 300 steps. Take basically a small model the model that you have taken last assign Train the same model twice for 300 steps. One of the cosign under WST and stop both at 200 right to put the losses and the state that you see your model in. sweep the learning rate at width of 256 512 and 1024 and plot the loss again the learning rate. Mark the three minima. State the value you would use for 496 and how confident you are in So essentially you thinking a bit about how the mu works. Any questions?

The Admin: This is one of the last session where as I said we'll have some theory left and post this the next one is going to be interesting one this is from here we basically start making our own code on the next one and next one from next one we'll start going deeper into the actual implementation of the whole model and probably next session we're going

The Admin: We start assigning roles and start making data sets and whatever we discuss we want to do from this point to this point. M

Mukund singh: Yeah, just one more of not exactly a question related to what you have taugh but just to understand how much of the mathematical details should we know while making decisions about what optimizer to use…

### 02:20:00

Mukund singh: what hyperparameters to use for those optimizers while implementing the model.

The Admin: there's…

The Admin: how much there's a correct answer to what you said and then there's reality the reality is that we do not have enough mathematical background or…

Mukund singh: Yeah. Mhm.

The Admin: even experience to be able to comment correctly what we want to say and if this was 2024 I would have said that do spend time in understanding Adam and other stuff but the rate other things are changing it does not make sense for you to go inside and actually look because you have AI agents to ask such questions can you prove mathematically this is the right thing for us to do that by hand it's going to take literally six seven months for you to understand all of what has happened here what I explained to you is literally 15 years of research combining together so…

Mukund singh: Yeah. Heat.

The Admin: what you do

The Admin: need to know is what is the side effectw is solving, why and how meon is better but internal mathematic is something that you should not go in once it's like this should you understand how the car works or how to drive a car which one should come first. So moment you have a good understanding of how to drive a car…

The Admin: then you can ask questions and go deeper.

Mukund singh: You got it.

The Admin: And this is the max math that is required for any of the sessions.

Mukund singh: Yeah. flights.

The Admin: All right.

The Admin: If you don't have any question then I'm going to see you next Saturday. As I said this probably was one of the most boring session and don't treat it boring because these things are important. you do need to know what Adamw and weight decay and other things are because you will be using them. you need to know why people did what they did the math behind it a little bit but you need to commit to the fact that you need to know the process. You need to know that weight decay is helping in what because these are like medicines right but we need to know what disease are we going to solve with this.

The Admin: So when we start training in the training I wanted to notice something is wrong our grains are going bigger for particular kind of weights and based on that what should we pick and what should we do with different heads a very simple example let's say we are training a 1 billion parameter model and then we see that our router which is going to route our experts is behaving very badly so we do a custom surgery we reduce the LR for only router and not everything else now it's behaving very well now we decide

The Admin: to train a bigger model. How do the learning rates transfer there? you have MU. what do you need to read about and how do we move forward with Any other it will come.

Anirudh narla: Sir, I guess slightly off topic, but I was just curious how do you plan to assign roles for 250 people or something when the training starts initial assignments is that…

The Admin: I've answered that question in the earlier sessions also and it is that I will force people to work on topics that I want them to work on I will not ask what is it that people want to work on all of you think that model architecture is the main thing it is not so based on how initial assignments are done or initial projects are done people get to choose finally good topics yes not the assignments the projects that I'm going to assign

Anirudh narla: how they performed in assignments?

The Admin: during the training. Correct.

Anirudh narla: During the training. that's nice. As you said, natural selection. Okay, that's what cool. sir, I also

### Meeting ended after 02:23:59 👋

*This editable transcript was computer generated and might contain errors. People can also change the text after it was created.*

