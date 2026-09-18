## **ERA V5 Session \- 2026/09/12 06:46 IST \- Transcript**

# **Transcript**

The Admin: Today might be a short session but this is one of the most important session when it comes to speeding up our training runs and there's a lot going on in the u outside world where the soda labs are. I'm not sure how many of you are following few questions for you because these are very important ones and if you ever went into a deeper training situation then what is at stake what would you be doing what you can do I'm not proposing you should do but you should know how the sa labs are training have you heard of the anthropics latest report how many of you following what anthropic published recently

The Admin: Second, what did you hear?

Sagar pallai: I'm in Chinese distillation happening and I is using those data to missile fire and

The Admin: So Chinese disting distillation till now people felt that like deepseek or moonshot or zombie they are directly talking to anthropic and taking a data right and using the training traces to train on.

The Admin: But what recently news that came out was the report secretly forwarding some users request originally sent to Kimmy to plot. So there's a massive search that is happening from China to figure out the leaked keys of Claude and Gemini and sometimes they officially get using some weird ways also. So essentially imagine that these labs are actually getting to anthropic and Astra and other models properly somehow either leaking the keys or maybe actually installing an account also. $200 give you a lot of communication with these agents.

The Admin: Kimmy is also selling Kim K3 has its own subscription to its own people. So when you're talking to Kimmy suddenly they will take that data and send it to clots whenever they know that they can't solve it or there's some problem that is happening and then training on that traces. how does anthropic know because some of the internal details that PLA was using PLA is Chinese military establishment they send the data for video analysis to Kim thought I can't do it. They send it to anthropic.

The Admin: So now anthropic has some secret databases of 18 Chinese organizations and lot of stuff but that is how these guys are actually getting the training material on and there's a lot that has happened the huis that are fighting with Saudi Arabia and others they designed some military equipment and crazy stuff now at the same time we have flash 4.1 from deepseek I'm not sure how many of you have used it. But that is a beast. That is something that really is very close to I'll say opus 5 or even fable sometimes at some levels but it extremely fast. if you have not used deepseek you do not know how fast it is right it's amazingly fast. The way my workflow has changed in the last u I'll say 10 days is very different. I used to be only on cloud.

The Admin: Astra came in I thought okay I switched to Astra blew my mind I've not seen anything like that much better than Fable especially in the v visual related task I exhausted all of my crits and then I saw deepse 4.1 flash I thought okay why don't I use it and now I used it what is happening now is the deepse processes things faster than my opus can so us has a full access to my codebase and I use opus as

The Admin: and basically guardian to control everything. decides that this is what your agent should do. I copy paste it to deepsee and by the time I look out of the screen deep is done. It's literally done and I take the response back to opus and opus takes double the time to think what should we do blah blah blah and comes back with its own thing and again gives it against I want to see where I am right now. Yeah, it's done. Right. So, I gave something to Deep Seek. It's done.

The Admin: I'm pasting back to opus asking what is the next task because I've not built a bridge right now between the opus but it's extremely fast and I want to show you that part also fact we may be able to find e 4.1 Opus versus Astra. Let's see what it says.

### 00:05:00

The Admin: And the

The Admin: Reason this is important at our level is there are multiple things that deepseek has done we will go deeper into the 4.1 paper when the time comes in but if you see they are saying that we have done all the optimizations we could on the speed side on something else side by the way people have already started trying to look at this and Astra and are not 54 or 52 tokens per second they are slower they sometimes go to 25 to 30 also right and this guy is consist

The Admin: consistently giving me at least 150 160 170 depending on what time of the day it is and that is a massive change by the time I can't essentially read what DCK is doing that is how fast it is so you give it command and the program it's done and at the same time if you have people who are trying deep seek 4.1 flash on Mac book What's deepseek is at least as good as over five and…

sonu agarwal: So based on your experience accurate speed is one thing what about the accuracies deepseek is able to provide or just taking the base from deepseek and then Okay.

The Admin: not confused.

The Admin: Deepseek is very direct and when you talk to deepseek you will know that it's actually a copy of opus because the way it talks right I know how all AI talks because I've talked to them way more than I talk to humans nowadays but I know the pattern in which they talk right and that is exactly opus so it is distilled from opas no denying on that but the speed and…

sonu agarwal: At least once I'm going Okay.

The Admin: accuracy is just tremendous right now I can't imagine that how good these Chinese model actually are so it's a eye opener for me that's why I'm sharing with you also and it costs nothing. yes,…

Suyash Patel: Yeah, because we are discussing this. I just had what harness do you use and if in general you can Okay.

The Admin: DC harness deep harness and DC harness with PST.

The Admin: So it runs locally. So compared to your clot code it's going to look something like this. So I've just started. So this is my full website that I'm launching probably in 2 three weeks And this is a part of the capstone that is going for okay let me show you how fast this is So Claude is saying okay paste this as the objective.

The Admin: Okay, took literally 5 minutes to think and copy pasting it. On the bottom, you're going to see the speed here. You're seeing 134 tokens per second. This is what it's saying. These are not commands, by the way. if I open up, it's saying things. So it's so fast you can't even see what is happening right now and it also gives trajectory of what happened how it's behaving what commands it ran full details essentially then what are turns that happened and what are the calls that have happened so here are the things it is discussing and finding context finding assistance so really mindblowing literally

The Admin: mindblowing and the speed wise you can see it's four times fast but at least I think it's something like five times compared to u where the bundles are so why did we discuss that so there are two three things that we need to keep in mind one is the deepseek architecture it's especially the latest one what they've done now is Raj I'm not using Deep Seek China.

### 00:10:00

Raj H: Do you think there would be some security issues if it accesses some of your other folders, your root folder or those things?

The Admin: I'm using Deep Seek US. So, these are open models, right? Anyone can host it. So, when I'm using it, I have made sure that I'm using only the US server which commits US server and yes, I'm not using Open router is very shady.

The Admin: don't use open router but I'm using Firefly I think Fireworks is based and they're used by people that I thought okay I can believe on Uber for example vers and…

Raj H: reason.

The Admin: Kursa so all of them using cursor is using it so you can understand that it's really good right and pricing wise so we can deploy try and take the services for training also we will evaluate that but if you see deepse flash right now this is not the correct one

The Admin: Yes, this is the pricing.

The Admin: This is cheaper than deepse itself. Deep that's 3 and then some other numbers and we are using serverless. So there's no server for that also, So there's no Chinese data going to China as a problem. Now this is the comparison as charged or…

Raj H: Okay, one last thing.

Raj H: One last, where can we find a small write up of how to install it, and all that stuff?

The Admin: Okay.

Raj H: 

Raj H: Thank you. Thanks.

The Admin: Here if you see the comparison terminal bench it does show slower than Opus and Deepseek 74 compared to DSVD. Then we have Cyber Gym again higher here. Auto edge.

The Admin: So in my experience at least as good as OP 5\. the things that we need to look on this particular model is that it's a half a trillion parameter MOA. We do not have budget to train something like that. But this is something which becomes achievable. I think error v8 will be able to at least train half a trillion model. That's how fast things might move at that particular time. Then we have a casual encoder only 8 billion active parameter for the input and 16 billion for the output. It's a very different way of looking at a thing. Generally we have the same parameters that are required to understand what is happening and then report on that right or work on that. But this is astronomical. Second is let's calculate a cost of 52 into 100\. So around 2.89% something around this is what we'll also target.

The Admin: So this is around 3% of the that are there for active parameter in the MOE at the next session. So we'll understand more on that. if you look here GPQA is more on the journal knowledge right what is happening blah blah new news and etc. But if you think about it most of the very complex things you can actually go online and find it right. but here also if we have Deepseek V4 Pro which is a bigger model that was a 92.4. So what they've done this time they focus more on exactly where people want to use it that is a agentic task and that is going to be programming and coding right so it's going to break there but if you see the V4 Pro which is a bigger model it's lower in that and if you see claude opus that is 93.4 GPD6 5.6

The Admin: This is 94 against these models they have a very good view of what is happening at a deeper level also they are the G gk essentially right I'm going to focus only in the coding part there if you see we have code forces 34 so these guys are not reporting so let's look at where they are reporting so here we have GPD sold 88 and claude opus 89 here this guy is 90 right 2.1 3.0 4.0 zero not so much difference in deep. here you're not seeing There's something called benchmaxing which is training your model to just train on the benchmarks and Gemini is doing that a lot and they're literally getting pushed out.

The Admin: So here you see deeply 74 really good there right sabism good there so overall model is really good but the biggest thing that they've done is on the KV cache now DC1 when the stock market already fell by a lot I don't know if you followed that news or not so this is the amount of bytes that was required for each token T2 they dropped it further flash they dropped it here and right now we are here the amount of memory it takes to keep in Even the memory amount of memory it takes to keep the older token of memory has dropped this much. That is massive, right? And people have worked it out to make it work on MacBook 128 GB. I heard 64 GB minus 64 GB. So I'll wait for that. I'll see if I can run it locally or not.

### 00:15:00

The Admin: So if you do read the technical report which here you'll see that they're talking about that we have reached an era where whatever is possible on the architecture level is sort of frozen we can't do more there right we have literally at that particular point and the reason of seeing something like that is of course these models are trained by AI only right of course the mathematical analysis and everything else that goes inside training and optimizing is done by AI at the back end so unless something magically happens with respect to completely new Architects are sort of stable. All Chinese model Kim K3 etc etc are following this. That is not to say this is not exactly the model for Opus or Fable or other Astra as well because generally industries tend to converge in terms of the overall architecture but this paper is very clear that the only thing that is left is data.

The Admin: you get good data, you get much better output, And if you were to hack, let's say, Anthropic or somebody else and get literally maybe 10,000 people into $200 is something like In $2 million, the amount of data you'll collect from Anthropic is massive. And that model, you can literally take your own model and upgrade it and change it and actually reach So reaching soda is not a big issue right now. The big issue is that how do we actually train it and Chinese are again Chinese. So they just did something magical. They took a Nvidia 1590 graphic card and put a 98 GB RAM on it. So this is getting crazy right now.

The Admin: So they're buying 1590 from somewhere putting a 96 TV graphic card on top of it. That means that if you now get a small box in that box you can add eight of them. and this is four lakh. India of course we'll add and multiply that into 1 point customs in 41 lakh you can build a super cluster in India on which can actually train massive models right and if you're a startup then take it to 32 and this is 1.6 cr so in 1.6

The Admin: six cr you are getting a machine that is impossible to even think of so the occurring times are crazy people who have resources they should deploy on these side but how do we train on multiple GPUs not change of context let's come to task because there's a lot we can discuss on geopolitics later on so if if you heard of alex net was one of the first I say revolution it was the starting point of the revolution of Till that particular point it was struggling the models was big and there was no GPU by the way. It was very difficult to train on CPU anyways and people had not figured that part out. So Alex key what he did was he had a graphic card GPU on which he was playing game. He was a PhD student also he thought okay why don't I merge this. He merged and he realized that I can't run it on my model bigger than the amount of memory that I have.

The Admin: So he was the first person who took multiple GPUs and showed how to train a model on that. We're talking 2012 is not far. When was 2012, 14 years ago? So that was the first time an AI model actually ran on a GPU and since then we have seen a lot. Now the way he ran is very different from how now people are running on the GPUs. We have something called in V4. model we went to 0 0 1 02 we tried all of them.

The Admin: So these are some of the basic concepts that you need to know and once you understand what is happening here then we can figure out an architecture which is supported by that because sometimes the model architecture itself cannot be sharded which we'll discuss what is it cannot be sharded on a multiple GPU right so didn't we thought we are making a best model and we're going to train it but ideally what should happen is that we should understand the hardware on which we're going to train it and the kind of model that we want to train and then merge it to make sure that we can extract

The Admin: ract as much juice as possible from the hardware itself right and that's where the session becomes important it's a slightly shorter session but I didn't want to mix different kind of things also right and each line is something that is important so we'll go through each one of them a single graphic card has a fixed amount of memory that we're going to be using graphic cards that have 80 GB 96GB 120GB and so on this GB is not the GB of storage so generally 80 GB actually means something like 74 or 73 GIB which is what we use for storage, right? So, the The larger graphic card available to us holds 80 GB. But we'll go to Blackwell series also specifically because we can train 4x fast on Blackwell even though it's 4x more expensive also

### 00:20:00

The Admin: per unit time. A model has 30 billion numbers in it. We assuming for example and every one of these numbers has to be stored somewhere when we train the model as we discussed in the last session also we have activations that we need to store and we have the optimizer states that we need to store. We have to store the back propagation state and we have to store the same model in the highest precision as well. when we say that we are training a model in a let's say FP8 or FP16 that doesn't mean we don't have a FP32 copy of it we have to still have a F fp32 copy of it and the reason is that we actually update the 32 model and then use the 16 model right because 32 model has a higher precision and sometimes numbers are very small to not be able to support in BF16 all as well so if you see what is happening is our weight is going to be in 16 bit format for the arithmetic

The Admin: when we say arithmetic we're talking about the computation that happens on a GPU by the way even before I go move forward do you guys know what is a GPU what does it do why do we use GPU there are many people who might not have a background so it's important because some of the later parts are on top of it everyone is aware of what exactly GPU does compared to CPU then what we do if just do a hands down so All right. Good. Okay.

Deepjyoti Saha: Good to have a prime

The Admin: What happens is this concept comes from CPUs.

The Admin: So when I need to multiply for example 4 into 5 into 9 yeah why not then 6 into 17 and 4 into let's say two right simple four equations now on a CPU runs on a clock I'm not talking threaded moment we multi-threaded that already is giving you two threads talking about one single thread of a CPU.

The Admin: So CPU is going to take this one give some answer then it's going to take this one then give some answer then it's going to take this one it's going to take some answer then it's going to give this one then you give an answer so CPU is a four cycle GPU a very very simple way of understanding what GPUs are that there are very very fast and big SIMD which is single instruction multiple data right so instruction in all of this is multiplier right so we multiplier So imagine a simple multiplication The kernel is the smallest computation block that you can create in a GPU. And the block is programmatic and hardware oriented also. So in GPSMD you can say that I have this vector please multiply

The Admin: And in single steps is multiplies. So GPU does everything in single steps. So what it really does is that we have one block, we have another block and then we have this multiplication kernels here. It will take four 5 6 and four 6 9 17 and 2\. And in one shot it's going to give you the answer whatever the answer is. That's for GPUs. It's a massively parallel computer but it can only perform one operation at a time depending on how complex the GPU also has a lot of code. So some part of the GPU can be doing different things. Now you talk about CPUs in octa core, 96 core, thread ripper and so on. But let's see even a simple I'm saying 100 h200 but let's look at our video 5090 justification. Look at the number of cores it has.

The Admin: You see that 21,760 CUDA cores. Those are running CUDA operations, right? And each of the core can run multiplication, addition or sometimes collection of a lot of things, right? So the GPU really is a massively parallel system that can perform same operation on. So it has drawback also because of how it works. Drawbacks drawbacks are that so you need to imagine a GPU always as a simple truck then you can understand whether your program is correct or not when you're working with a GPU right so it's a truck you can send a single toothpaste or you can send a box of thousands of toothpaste or toothbrush together now the drawback of GPU is that if you ask a GPU what is 4 \+ 6 equals to it's going to take let's say 0.1

### 00:25:00

The Admin: second to calculate that 4 \+ 6 is equal to 10 and if you say 4 \+ 6 and like that you have probably 1 million rows it's going to take how much time anyone same time so this is the drawback so…

Avnish Midha: Same

Kunal Sinha: Same time.

The Admin: if you do not fill the GPU memory brim up to maximum what can calculate you're actually wasting it right and that's where the calculation and good structuring of how we are trading the model on how occupied our GPU is very very important. We're going to use some of the ratios to figure out such things right. So GPU really is lot of data. So this is a sequence of data that is coming in. You define what operations and this is a good time to explain what kernels also are. So let us say we have a sequence of data. We have the sequence of data.

The Admin: we first are going to be mult adding this data and after that let us say we're going to add whatever results we get I'm drawing it essentially that's a good idea so I'm drawing it so whatever results we get from there we're going to be multiplying with this data shapes need to be same that's why I'm trying to keep the length similar so let us say this gives us this data we are going to be let's say dividing it by this kind of data okay so if you do not optimize it for a CUDA or for a GPU then this is one process because it has to wait and save the data somewhere so this is where the data is saved then this is again second process and

The Admin: This is again third process but a kuda kernel whenever we say that we have a GPU kernel what it does is that it get rid of this intermediate state. So this whole thing becomes one operation in memory itself. The data is stored and in one step everything is done. So it's a single operation where the data does not come out of the sam that we saw in the earlier section right. So that is actually what GPU is massively parallel computer on which you can perform a lot. So what does it mean? why do we discuss that? We discuss that because now the same graphic card we have a model and we using eight of eight let's say models and each model has bat size also. So we have eight copies further right you need to remember it when we say we have a batch size of eight. Let's say we're talking about one GPU and we saying we have a bat size of eight. What does it mean? We have eight copies of the GPU of the model in the GPU. Are you clear?

The Admin: It doesn't happen magically that we say a batch size of eight and suddenly same model can you have to have eight copies of the model in the GPU or of the RAM that we have right so if you say our batch size is eight and we say that we have eight GPUs we have 64 copies of the same model in the overall storage right so the batch size bigger than required that's the reason the bigger batch size required so we need 16 bit format because that's what We are going to be storing it and arithmetic is better. There we have all the gradients that we are going to be saving and changing because we need to know what the old gradient was. We require it for further calculations. We're going to keep a 32-bit copy also. This is for accuracy. This is where we actually add and subtract weights and update it. This is used for backward calculation. This is the copy that we keep on updating. And then we have the two running averages that the optimizer keep. Right?

The Admin: So overall we have 16x for one single parameter that we have. what this means is that if you have a model something which is let's say 27 to 30 billion parameter is going to be causing something like 447 GB of data and this is GIB. So this is when we save the model. So GB is the actual number that the GPU has 80 GB graphic card etc. But this is the actual amount of storage that it has from the story savings perspective. This is not true by the way for this section. I plan to calculate around 27 to 30\. So if you

The Admin: have 80 GB cards then before single calculation is performed we are out we can't even save that kind of model right that we can't push even a 30 billion parameter model in 80GB card we clear on this or a 30 billion parameter model needs 447 GB just of one batch we are not discuss even more we can't keep it inside a 30GB graphic card by base basic calculations, Okay. So that's the problem and that's why this session exist. Now there are some things that you need to know before we move on. the GPU is a graphic card. Of course that it is what is going to be used for calculating the units of computation we have.

### 00:30:00

The Admin: In this session we using 80GB because it's easier to calculate but Maxwell and other if you see for example P200 specification this is the one that we'll be using for training. this is B200. It has 4 DB of GPU memory band. One second. Yes. So overall 144 0 which means 1440 divid by 8 180 GB of RAM per graphic card right. So when we'll be using AWS when we buy this cluster we are going to get something like 1.4

The Admin: 4 terb of overall RAM different computers spread across different 8 GPUs. Now I do not have guts to go to FP4 training. So we'll be getting stick to somewhere around So FP8 performance we have something like 36 beta flops of computation. Peter flops used to be the supercomputer numbers in 2010 and today yeah it needs of power 14.3 kilowatt is good enough to run one big CNC machine I don't know if you are aware of that inside it has Intel and other class that's fine also we have 2 TB of RAM this is around the RAM that we will be needing for opening the database sharding it and etc.

The Admin: So this box basically is what sits inside AWS right good speed we're going to talk about speed today because there are two different kind of speeds that we need operating temperature is cool 10 to 35°C right so humans are not able to work in this temperature but this GPU needs that temperature and people make sure the GPUs are getting that temperature it's a privilege to be a graphic card and AI today so a node is a physical machine holding server GPU is almost always eight that's the B200 that you saw so S200

The Admin: B200 depending on where the pricing are and what size the model is right so it doesn't make sense to take a small model and train on a B200 and just waste right so we have to be methodical about that the world size is the total number of GPUs that we have so let's say we go with a three cluster into eight is 38 24 GPUs overall that we have process rank is used somewhere else also but process rank is literally which GPU in the cluster of eight or 32\. why do we even need to know the process Interestingly when we use this 0 0 1 02 what is it? We will discuss in a moment but whenever you use this algorithm 0 1 02 03 04 the 03 sometimes one GPU have slightly more compared to other and a slightly more might cause it to crash. So we will know that your process rank four crash.

The Admin: So you need to know what is the meaning of that. So of all one GPU has crashed or one GPU has caused a problem in saving the checkpoint. Right now when we're making a model there are 10 MB 14 MB maybe 100 MB. So you're not facing this problem when your checkpoint is going to be 1.2 terabyte of storage then you will know that what is that we talking about one GPU just failed in saving a checkpoint and whatever computation you have done for the last 4 days is gone because the model is not recoverable. It is training by the It's a very interesting thing. The model is training because training is going on. But while saving the checkpoint, GPU did not save the weights properly. So now you're confused. What should we do? My next checkpoint will actually save or I should kill and waste my two days of computation which is a lot. Now interconnect this is what we'll be focusing a little bit today on. Now interconnect is a wiring that carries the data between the GPUs. So now we on one node we have eight GPUs. They need to share data amongst themselves.

The Admin: This is called NVLink. So when you see your logs when we start training you're going to see the NV link is up and so using NV link version X. There we are talking about 450 GB per second. Now this is important because and that's why we are sticking to this calculation. If a model size is around 450GB and we're getting around 450GB per second that means it takes around a second to swap the model from one GPU to other GPU. Are we clear? That's the reason of taking these numbers. If you're using NV link then we get somewhere around 400 GB per second which means it will take around a second or 1.3 second because here is So somewhere around 1.3 second to move a model from one GPU to other GPU and we'll know very soon that why are we talking about moving a model between GPUs.

### 00:35:00

The Admin: But if you have taken two nodes, these nodes are not on the same machine. Now they are connected with a wire, This is not fast enough. And there we have around So 50 GB per second sounds a lot like our internet connection and etc is too slow but 50 GB per second is nothing when we have a model of 150 GB right and that's a very very important distinction because soon you're going to see that we are going to be moving the models from one GPU to other GPU and that is required we're not going to be moving the model we're going to be moving that kind of data from one GPU to the other GPU because back propagation we need to move weights optimize states we need to move that a lot that we need to move

The Admin: So the problem comes in that we have 450 GB per GPU right node communication using NV link when we are in a box but the moment we go outside we get somewhere around 50 and it's actually even slower depending on whether the server is heating up or not whether AWS has given a good air condition for the whole system or not. So we get nine times the smoke speed. So even though more than one node gives us more computation but it slows down the interconnect communication. So it's a very difficult thing to even answer properly right if I'm on a single GPU cluster single which is let's say a node of eight I'm rushing through my model is not fitting that particular node.

The Admin: So what I'll do I'll take one more node but the problem is that these nodes have to calculate and the calcul and the communication between these two node is nine times 10 times slower. where is the speed? So you get the possibility of training a bigger model but the speed is slow. It's very important to understand the collective is the operation that every GP performs run together. So collective is basically what is happening right now it's inferencing it's model training or calculating back propagation or something like that. So these are terms that we're going to be using. understand what is this P? P is the size of the complete copy of the model's parameter. So let us say our model parameter is P and that's how all the other numbers are derived from that. for 30 billion parameter model we're talking about somewhere around 60 GB and communication in this session is always measured in terms of P. So we're going to talk about how many P's, right?

The Admin: 01 is XP, 02 X is YP and so So cost 2P means 120 GB is going to be crossing from one GP 1 GP to other. Right? remember that part. What is P? P is essentially the cost or the size of the model and we'll talk about how much memory we need to transfer from one GPU to other GPU using these P numbers. the data paralism this is exactly what Alex did in 2012\. The simplest way to use eight GPU is to give each GPU its own copy. Right? Every GPU has its own copy.

Sumsum Sunny: I can money.

The Admin: If we have eight examples of eight batches, then each GPU will have eight copies of the model and we have eight GPUs. So we have 64 copies of the model that we have. Fair enough. So we send the data to all these 64 models that we have. We do the forward propagation. what should happen? Back roation.

The Admin: Right? The loss calculation is happening and we need to calculate the back propagation on all of them. So we have the 64 back propagation that are happening and somewhere we need to average them and save and actually calculate the average back propagation for the 64G models. Then we need to calculate the weight updates and then we need to update all of them. That's where the interconnect is actually required. Right now this is the drawback of the GPU also. you are going to see that we're going to be performing some calculations on all the GPU that you're going to see.

The Admin: We could have done that on single GPU right but the problem is can't when you connect eight GPUs they're exactly same copies so we will have redundant calculation that we must do and we have to do because there's no running away the amount of time it takes to disconnect a single GPU node from seven GPUs let's say have eight right amount of time it takes to disconnect one GPU from eight and say that GPU number one why don't you do this while seven are not working it slows down everything so that is why I'm saying it's the easiest way to understand how P is Imagine using truck for your life. Why don't you go to office in a truck? You will actually enjoy it. Especially if you're in Bangalore, Roads are anyways bumpier here, but you have a bigger tire. So, you need a bigger hole to disturb your life. Then people are going to be afraid of You'll be sitting much higher than the most expensive SUV also. But imagine moving around in that.

The Admin: you're going alone in office parking it somewhere right but if you're taking 100 people then life is different if 100 people so why again the truck analogy right so let's say you want to stop for a pee break all of those 100 people also have to stop they might not be going out and peeing at the same time but they have to stop right your truck goes bad means all those 100 people are also not disturbed that's why it's a very very important analogy that I wanted to keep because every time you ask one of those 100 people to do something, the whole truck has to stop or whole truck has to do exactly the same thing. So the simplest way to use AGPU is to give eGPU each one of them a copy of the model. We've given that and a different portion of data. The data comes in based on the batch that we have or we're training on science or sunscript. Now each GPU reaches its own examples run through its own copy and produces its own gradient.

### 00:40:00

The Admin: Those gradient differ from each other because we gave different examples. Here was a math example. Here's a coding example. Here's a geopolic example. because each GPU saw different text. Fair enough. Now the copies are then so we have essentially brought back into agreement basically means every GPU sends its gradient to every other GPU. Don't imagine that we have now CPU sitting in between a manager. You have a GPU. They're calculating back propagation. The data moves to CPU calculates average. Definitely no.

The Admin: You will not get CPU is a scooty in front of a truck. Cannot do anything right. And the amount of time it takes to move data from to GPU is also very very slow. So we are not going in that way. Which means every GPU sends his gradient to every other GPU. That is where the magic happens. that is where the 01 02 and other things are going to be discussed today. So every GPU you have your gradients. I'm going to send it to you while at the same time you're sending it to me. So now you have my gradients and Alternatively, you could have given me your grad I could have averaged and given it back to you. GPUs don't trust each other. So everyone needs every other information, How do we exchange? For example, on Olex somebody selling you iPhone for 50 15,000 rupees. you're going to meet the guy. You're going to give money from one hand. You're going to take the phone from one hand and then leave. what GPUs do, So every GPU sends this gradient to every other GPU.

The Admin: All of them compute the average and each applies its own update to its own weight. weights are same initially. So if I calculate the gradient, you also calculate a gradient mathematically going to be exact and we're going to be performing exact updates to a weight. Right? And because they started identical and apply the identical update they remain identical. This is data parallelism. Very important. understands subtle differences that might not hit you when you work with GPUs or CUDA programming but here every operations happens on every single GPU super important to understand give me a thumbs up if you understand this right the way the computation is going to happen on GPU is that all of them will have exactly the same data after exactly all the same steps and all of them will compute and you can think that this could have happened on GPU number one because average is going to be same for all

The Admin: But the way GPUs are designed, the same operation must happen on all of them. There is no running away. You can't stop seven, make one GPU compute and you've already stopped seven. It's a waste of time again. So we don't waste them. We just run them exactly at the same time. So the averaging step is what makes the arrangement correct because everyone gets exactly the same data to averaging the gradient from eight GPU each of which has process cert sequences produce exactly the same GPU which one GPU could have also done the distributed run is therefore mathematically equivalent so there's no disturbance there or there's no miscalculation that what if my one GPU calculate something else compared to other GPU that won't happen so the batch optimizer sees is the product of three numbers we have the global batch is going to be calculated

The Admin: ated from three things we have sequences per GPU. So then we have GPUs and we have accumation steps. So if we have taken let's say 8 GPUs and then in that we have let's say into accumation number of steps that's the overall global batch we have. So all the GPUs are going to wait for global batch size step and then calculate the gradient. Right? So that's the overall data paralism that essentially goes inside making 0 0 1 02 really practical. Okay, sir.

Syed Abdul: So in case you said where during back prop each GPU gives the gradients back to all the other GPUs. Isn't that a factor seven has to talk to one then two has to talk to 3 4 5 6 7…

Syed Abdul: then three has to talk to four five six seven won't it take so many steps like eight fac okay so there are algorithms for Yeah,…

### 00:45:00

The Admin: What do you mean?

The Admin: Yes, exactly. It will. And that's where we have 0 1 02 03\. how do we speed that part up that's the next session. But you're right. if we have eight GPUs and all of them have to share the data then we have to wait for based on the discussion 450 GB model and we are saving that let's sharing that state so 450 has to move seven times right because 7 GB of information has to come to one seven steps right eight steps I know so

Syed Abdul: that's for one it has to say. Then for second it has to do for six. So 7 6 5 4 3 2 1

sonu agarwal: So during process rank you mentioned eGPU hold slightly more compared to other. and during this aggregation time what are the possibilities of running into out of memory or some kind of issues where

The Admin: very high.

The Admin: That's why unfortunately we can't push it to in V4 we pushed it to 94 95\. So you're literally seeing the tax and you're not happy and you're afraid also because if two GPU in the run while you're sleeping goes out of memory are gone the whole data is just corrupted that's why more checkpoints but we did push sometime it went to 98 also but 94 95 was our top line we didn't move beyond that and it's not that it takes more sometimes what happens is you have some checkpoint saving

The Admin: So GPU has to do slightly more work. Sometimes we calculate some statistics. For example, we calculate how the MOEs are behaving. We have that. Sometimes we want a gradient statistics. So we want to calculate that also. that is what happens, right? And…

The Admin: because all the GPUs are holding the same data, you're not asking eight GPUs to give me the gradients. You're asking one GPU token you give me the statistics. That's where slightly higher peak happens. So we need to be very careful of those. We can't use 100\.

sonu agarwal: So when you are saying 98% this is a total capacity of each GPU that's…

sonu agarwal: what instead of using 100% We can profile the GPU and…

The Admin: No moment you use 100, you are locked. because then the 100 can be used in inferencing but not at we can't use in inferencing also because if you do 100 that means that you've occupied the whole RAM.

sonu agarwal: 

sonu agarwal: see how much memory we have connected…

The Admin: No, of course we'll do that.

sonu agarwal: till now.

The Admin: But the point is that there's no way we can calculate it how much amount of they are going to be running so fast that it's possible two three operations might happen at the same time and slightly more view is required not experience it has to come from test.

sonu agarwal: So it's like it has to come from experience how much data we are throwing in each.

The Admin: So we'll test and we'll test. So there is no exper there's no book for following this So what moment

MUHAMMED ROSHAN P: Yeah, when a GPUs are there, So if you want to share the data with all the GPUs, it's like it will be taking too much time, Then why can't one GPU take the data from everything and average out and distribute others? Why we are let's say it's complete permutation, right? We are doing

The Admin: Who will answer this question? Okay, somebody needs to answer this question. Who's going to answer this question?

Syed Abdul: So the time it takes to stop to send and…

sonu agarwal: What was question? Sorry.

Syed Abdul: then it's more like waiting than actually doing everything because it's parallel. So one doing all takes the same time and…

The Admin: …

Syed Abdul: stop and resume.

The Admin: so we have GPU number one. I'm only going to take GPU number two and GPU number three. And this is time. Okay.

The Admin: So they have done the computation. So you're saying that why don't we send its data to this guy. So we are sending its data to this guy.

The Admin: And then you're saying that why don't we send it data to this guy. We are sending its data to this guy. It has to happen in sequence or we have enough memory that both can happen Let us say it happened in the same step. So this is at step time. What are these GPUs doing in that time? I don't know. And when you write algorithm you write in such a way that GPS is not added.

MUHAMMED ROSHAN P: Okay, we'll be item.

The Admin: If they were to calculate exactly the same thing what do we lose here your GPUs are silent not doing anything.

MUHAMMED ROSHAN P: No, basically we lose some time only here, right? Nothing.

### 00:50:00

The Admin: But my question to you is if I use the GPUs to do exactly the same calculations what do we lose?

Varshith Chennuru: Nothing.

Mukund singh: Nothing.

MUHAMMED ROSHAN P: Thank you.

The Admin: What do we gain?

Kunal Sinha: Parallelism.

The Admin: No, that's the important part. Let's say the addition has happened. In the next time step, we have the data ready. And now that data has to be sent to these that is saved that is…

MUHAMMED ROSHAN P: Okay, got it.

The Admin: why all the operations happen on all the GPU at the same time because the final calculation doesn't have to be saved back again anyways you're keeping the GPS idle at the middle so this step is not required that we calculated here already right amount of time it takes to send it all

MUHAMMED ROSHAN P: But there will be time taken to send the data to all the GPU, So that time also we need to consider here, right? Okay.

The Admin: all the data to one GPU is same as sending it back to those GPUs also.

MUHAMMED ROSHAN P: It's okay.

The Admin: So I think no that happens here.

Swati Bansal: So isn't here where kernel could come into picture where all the computation was happening in the kernel concept when you mentioned that we compute all the operations in memory and then send it back in one go. So, can't we use the same concept here?

The Admin: What has happened is now we have the results here. Those results have to be mapped and results are sitting on different GPUs. When we discuss kernel we discussed that we have data 1,…

Swati Bansal: Uh-huh. …

The Admin: data 2, operation one and then operation two,…

Swati Bansal: within Okay. Got it.

The Admin: data three. This can become a kernel not on sitting on a separate GPU.

Swati Bansal: Got it.

The Admin: this be.

Swati Bansal: Got it.

The Admin: So now everything is lost.

sonu agarwal: So now this exactly similar data are sitting on all the GPUs during the aggregation and during this aggregation calculation. Suppose there is a corrupt data got corrupted due to some reason on one GPU. So can we just avoid that GPU because other has the similar set of data right so we can not aggregate based on how much Okay,…

The Admin: The speed at which competition will happen is that you will know that corruption has happened. and you will know the corruption has happened after all the GPUs are done. It's like in a batch of eight biscuits one is bad but you will only know after you essentially are ready for packaging.

sonu agarwal: we cannot do that way.

The Admin: Yeah, N.

Nikhil Shrimali: But Rohan if we have the data timestamp and tracked in the schema that we have discussed before we would know which batch of data went corrupt and then we can re persist all of the others and then maybe we can train the data once again.

The Admin: But okay, what is the meaning of corrupt here? we have discussed a lot about the models. When you say corrupt, what do you mean by corrupt?

Nikhil Shrimali: By corrupt I meant that the GPU might have gone out of memory.

Nikhil Shrimali: There is some issue with the gradients that went into that GPU. Okay.

The Admin: So the old thing is we have one GPU,…

The Admin: we have 3 GPU. We are processing something on this. Let's say this went home. Then we can decide.

The Admin: side as you're saying not to use this uses data that is correct. This is old here but the capacity here is that the model size that we can store probably is something like 1x the new that we are discussing there we have 3 GPU if this is correct all our own bad according to you but we have something like 30x to 50x the capacity of the model so you lose some so the new algorithm we are going to discuss there we cannot do this this is not possible if one GPU is that means all the GPU home…

The Admin: but we get 30 to 50x the capacity of what is possible. Clear?

Nikhil Shrimali: Okay.

Nikhil Shrimali: One more Rohan. So if we are distributing the weights when we are aggregating let's say we have eight GPUs. So every GPU would have to aggregate the gradients of all the other GPU.

Nikhil Shrimali: Would we have that much memory available in that GPU?

The Admin: That's why we're going to be discussing things like zero in a moment.

The Admin: So we are at the older architecture still understanding how the old architectures work but we are focusing on a data paralism here. Right. The weights we have on each GPU are same that is a starting point. Right? So 3.05 node is 3.05 05 notice 3.05 notice 3.05

The Admin: 05 exactly same the data we have is different as I mentioned these are SINDDS single instruction multiple data data we have is 17246 so all the datas are different here the gradient that we calculated are again different here right all the gradients are going to be shared with all the other GPUs they're going to be calculating the average of all the other gradient that are coming to it and…

### 00:55:00

Nikhil Shrimali: Yeah. Heat.

The Admin: it's going to update the weight that we have right so data is different grain is calculated and all the weights

The Admin: are updating at the same time. Are you clear on Everybody else this step is important. All the gradients are shared with all and all the GPUs do this redundant calculation of if you do not do this redundant calculation then one GPU will calculate we'll lose one more clock and then save and then send it to other GPUs where the three GPUs are getting the data to update while the GPU is not sitting idle. So we cannot have that condition. We have to run as fast as possible. So make all the GPUs calculate everything. Okay. Now we have these collective operations and you need to understand that's slightly tricky to understand but once you go through this then we can discuss more and when you're writing your own algorithm especially on the data paralism with your let's say opus or cloud they're going to be using these terms and you need to know what these are.

The Admin: If you had done Python programming or something on Python or optimizing speeds on Python, And you would already be aware of it but humans are not going far away from Programming is TX. It's old. So first thing we need to know is something called All reduce is a term that means we combine a value from every GPU and gives the combined result back to all of them. Are we clear on this? It combines a value from every GPU and gives the combined result back to all of them. Average ingredient is an all reduce. Can somebody explain this?

sonu agarwal: It's like aggregating if there is a aggregation like addition it will aggregate it will take out one value and…

sonu agarwal: then distribute again to all the GPUs.

The Admin: So correct.

sonu agarwal: It's like 2 \+ 3 \+ 5 10 and then it will again go

The Admin: So the all reduce operation is that this GPU and this will happen for all four of them. This is going to take the data from all the other GPUs, it's going to calculate something and it's going to give it back to all the GPUs. This process is called all reduce. Are we combines a value of every GPU.

Varshith Chennuru: So is this the same step that we have done before step

The Admin: So it's combining the value of every GPU and gives the combined result back to all of them. So it's going to give the combined result back to all of them.

The Admin: This process is called alt reduce va that's a concept here we have a lot other things also going on gradation is saving the gradient for later stages we are not talking about that that can happen on a single GPU that can happen on eight GPUs at the same time also okay so this is all reduced

Vedapragna: Is this similar to the gradient accumulation we talked in last session? Okay. Okay.

The Admin: Let's talk about Reduce scatter combines the value in the same way and gives only one slice of the answer. Eight GPUs each end up holding 1/8 of the average result. Very important to Read it again. Reduce scatter combines the values in the same way and gives only the slice of the answer. Eight GPUs each end up holding 1/8 of the average result. Clear on this. We'll explain this in this you combine the value in the same way and give each GPU only one slice of the answer. If you have eight GPUs each are going to end up holding 1/8 of this result. Seth X.

Syed Abdul: And I saying you will experience. So basically it takes this sum and then divide it by eight and give those 18 value to each same like all but instead of giving the full value give 1/8 value.

The Admin: Max,…

Max: sorry even in all reduce and in this reduce scatter as well you mentioned that combines the value is combined which GPU combines those values is it a specific GPU or do all the GPUs so all GPUs will calculate the average and…

The Admin: all Correct. It's a part of a step.

Max: then return to every other okay thank Okay.

Mukund singh: Yeah, why would you reduce a scatter? how would it help?

### 01:00:00

The Admin: It's just a part of a step. There are two steps involved. In fact, in all reduce also, if you remember, there are two steps that are involved.

The Admin: It is reduce scatter and it is all gather. that's where basically I'm about to write all gather is the reverse. one slic Each its own slice ends up with a complete set assembled from everyone else. what is Combines the value. So it is combining the value and gives each GPU one slice. So reduce scatter plus all gather becomes all clear on this all reduce is what we're interested in.

The Admin: So keep in mind that this is what we want to happen and you'll soon understand why we are discussing this right because this is really the magic how deep can in fact deep speed there's thing called deep speed we're going to be using deep speed today which is what Microsoft invented and zebo is their innovation. So now you have a question.

sonu agarwal: So just I have one confusion. So suppose there is aggregation and h aggregation is happening after aggregation we are receiving a matrix. Now the all after doing all after adding everything if final output is a matrix then reduce sca will scatter the matrix or… the values. I mean if I have one by 10 and maybe two GPU initial five will go in one GPU in next five will go another one like that.

sonu agarwal: 

The Admin: We're talking about the whole data that is in the GPU.

The Admin: So it's not that I'm scattering the data itself. I'm scattering it to multiple GPUs. So the detail the reduce scatter followed by reduce scatter followed by all gather produces exactly what an all reduce produces and we want all reduce very soon. this equence is the reason that the next two sections are going to work. It also is going to explain the cost. operation all reduce each GPU starts with a full set of values.

The Admin: In all reduce each GPU is going to start with a full set of values and a combined full set later on. What happens in all reduce we have this and we're only talking about this guy but the same operation happens for everyone. It is going to send its own values to these guys and it's going to receive all reduce a full set of value the reduce scatter a full set of values are there. So 1 2 3 4 they have the full data that they want but they end up with a slice of the combined set which means that they are going to receive only a part of the data. I don't know how do I say so let's say this is how we're saying we are getting only the part of the data. The reason we're getting the part of data is because they're computing parts only. Right? Our simplest way to understand this is imagine we have four GPUs. Okay.

The Admin: This GPU is holding 1/4 the first quarter of the model. This GPU is holding the second quarter of the This GPU is holding the third quarter of the model. This GPU is holding the fourth quarter of the model. Are you clear? Let us say our neural network had four layers. We are only the fourth layer on the fourth GPU. And we When we forward propagated, you need to think four batches happening, how we do this? This is very interesting and that all of this is about to come later on but I'll just bring a precursor to this so get some idea where is B. So we have GPU So just GPU 3, GPU 4, right? And this is hosting layer number one or layer number one and two for example.

The Admin: This is hosting layer number three and four. This is hosting lay number five and six. This is hosting layer number six and seven seven and eight So we have a eight layer G network divided into four GPUs. Right? And this is how we have to divide it. Now goes inside the first GPU and you'll see that here we have four GPU sitting idle. We'll come to that. The goes inside the first GPU. Only two layers are required to compute. Once that computation happen, it's going to send its data to the GPU number two is going to perform the third and fourth layer. And after that, it's going to send the data to GPU number three is going to perform data layer calculation for five and six. And then it's going to forward the data to GPU number four. And we have seven and eight happening. Are we clear? Now when we propagate back propagation, this GPU is only going to perform back propagation for itself. It has performed back propagation.

### 01:05:00

The Admin: All the GPU is only performing backations for itself. Please tell me you understand till now. Show me your hands up. Right. And now what needs to happen? All of these guys need to communicate. And they're only going to be updating their own weights. We're going to go deeper. But here you see only one operation. But magical part is we could have done something interesting. We could have done something like this. This is GPU number one back again.

The Admin: Are we clear Can you see that if I just move the layers of the model in four GPUs in a slightly staggered the second quarter and second one for the first three steps. Of course, all GPUs are not occupied. said this is what I lose. But after the first three steps, every single GPU is always busy but always computing only a part of the neural network. Are we clear on what I drew? I use many colors for you to understand. This is what we're going to be discussing. And that is why we need to reduce all scatter conceptually. you're not going to be writing 020\. They're already very very optimized. Any question what happened here? Right.

The Admin: So the United is going to go inside this and United is going to be computed like this. States is going to go inside and going to be computed like this. So all GPUs now do not hold exactly the same state of the data at every single time steps when we stop for let's say something checkpointing of course we are again going to lose this particular time but this is going to run so many times in sequence that this part and this this is nothing we would process 160,000 tokens and in that we losing six time steps so barely anything compared to millions of time steps that we're going to be spending

The Admin: Correct.

Nikhil Shrimali: Ro, you said that each GPU will compute its own gradient but in the chain rule the behind steps are dependent on the ahead steps, Okay. Okay.

The Admin: So again, the data is going to be sent in a slightly different manner. We'll see that. Don't worry. time It's a timing question. said correct…

Syed Abdul: Yeah. Yeah. So when you say the event went in the one the United second is it like one sequence or in the same sequence tokens going the entire sequence goes in the input right?

The Admin: but it's still sequential only right to calculate United States off I need to calculate

Syed Abdul: So this is so during training.

The Admin: the United is still sequential only right we are in session 12 can't be saying that it is parallel…

Syed Abdul: It's all parallel. We send all of them at once.

The Admin: how okay maybe others also have this doubt how many of you think that the processing happens in parallel we are learning GPT these are trans progressive is the word generative progressive transformers Which means to calculate the n \+ one I should have calculated n.

The Admin: To I should have calculated n minus one.

Syed Abdul: Yeah, but that's but training we already know all those values for example during training for entire let's say example of contextment of 100

The Admin: What do you mean?

Syed Abdul: what are the next tokens for each of them and then you directly send all of those 100 and…

Syed Abdul: then directly calculate on all 100 tokens. Okay. Yes.

The Admin: That is me leveraging the fact that I can do it…

The Admin: but the sequence can't stop right I still have to calculate the back propagation of the United States of America and before that all of the others must be calculated in a GPU right to answer your question in your words what you're saying essentially is that I can block these in advance while training and I agree with

The Admin: That's what you're saying. but these are still non time step side.

Syed Abdul: Okay. Yeah.

The Admin: That's what you're saying, right? The…

### 01:10:00

Syed Abdul: Yeah. Yes.

The Admin: because how going to sit on the time step. The United States of America is in the war with Iran. So this is going to be sitting on multiple time steps and then it processes in parallel. So now if that part is clear. So let's see what happens in chunk. So GPU GP2 is holding 1 0 0 and GP3 is holding 1 0 0\. And we are keeping things simple. So we can calculate triple 1 2 3 4\. Now in all videos this is what we do.

The Admin: The GPU is zero two is going to hold triple two sorry one is going to hold triple 1 triple two is going to hold triple 3 and three is going to hold triple 4\. In all gather we're going to move data to everyone. So this is starting point in all d this happens and then in all gather this happens. Every GPU is holding exactly the same data for everyone. So we take a model this is the way we don't want to work. let's say we are in this particular state this happens. So all GPUs hold different states and then it's spread across everyone,

The Admin: This is literally the calculation that is going to happen every single step when we calculate our models. And what is all reduce in all? We have one here in Chunk 1 2 goes to GPU 1 that goes to GPU 2 that goes to GPU 3\. So you see what happens here. the same thing that I was drawing using those block that happened here. Clear. So we are at this stage. So when this is calculating it will send it chunk one data to GP1. that has information. In the next step GP1 is going to be sending the GPU 11\. So 100 is going to become 111\.

The Admin: And then in the next step GP3 is going to receive 111 from GP2 and that set is going to become 111\. So in four cycles all of the GPUs have shared all the data right and now in six step we have finished the overall calculation. But what this has done is it has allowed you to split your model into four different GPUs. Are we clear on this? yes or no. Hand down. So this is the magic basically behind all the GPU communication that is required. why do we discuss this and what is the cost of doing these kind of things. So that's where the cost of communication comes in. Now sending the GPU data between the GPU takes time. If the GPUs are connected in a single node it's fast but if they are outside then we are going to be using something like infin or something else So let us say we have a model of size 60 GB. We're going to call P as 60\.

The Admin: data palism moves around 120 GB per GPU on every single step. We saw 450 also for H200 but let's say here we have 120GB. because we want to keep calculating things simple. Our model gives P of 60GB. Data paralism moves around 120 GB per GPU per step. Wiring inside a single machine carries that in around a quarter second. network capable between machine carrying 120GB is about 2 seconds and a half. Okay. So let's say we have a path.

The Admin: So let's say we need to move around 2P to double the size of the model which is around 120GB. If you want to move 3P which is going to be around 180 GB the NV link which is the connection between GPUs in the same cluster we're going to spend somewhere around 0.27 seconds depending on 450 GPU per second we discussed earlier right so 120 divided 450 something like 2.7 seconds okay so within a GPU moving this data is 2 27 second time. If we were moving 180 GB then we are going to be using infinity band which is a interconnect between a node we spend around 2.4 seconds 10 times slower. And if you're moving 180 GB then we're going to be spending 3.6 again.

The Admin: It might seem u weird that why are we discussing something like this right and why do we need to discuss it becomes very clear when we look at the insane math that we have to work with what is the math that we're talking about math we're talking about is that we need to calculate amount of time it takes for let's say one batch can be one global batch might be let's say 32 for us Now, so we're going to be optimizing which means we're going to be writing kernels and all the other stuff and we're going to be seeing how much time it takes for one single computation, So when we are working on 01, 02, 03, we're going to realize that our speeds are going to be very different. Let's say normally we can't even fit our model into the GPU.

### 01:15:00

The Admin: when we move to 0 01 and 02 speeds are going to be changing. So let us say zero speed gives us something like 10,000 tokens per second. this guy gives us to something like 20,000 tokens per second to 20k tokens per second. And we move to something like this. This might give us something like 18k token per second. You can see that I'm not writing these numbers as They're not better always in terms of speed. Sometimes this might actually go to 8k but it is still considered. Why?

The Admin: because in this ratio maybe we can only fit a 15 GB model or 15 billion parameter model right in this state let's say this state we can fit a 15 billion parameter model but it allows us to go to something like a 100 billion model but our speed is going to drop right so we need to consider that also and here when we go we realize that we can actually go 120B also but our speed is going to be lower compared to this guy. So all these numbers are something that we need to be careful about because we can't leave the RAM. So we going to optimize the RAM. What you need to remember is we are going to be optimizing the RAM usage of the GPU not the computation it does. It's a very different way of looking at the problem because we are RAM bounded. We are not computation bounded. The bigger model you can fit inside more calculations can do. But that also means that it's going to take a long time to save the data.

The Admin: it's going to take a long time to move the data from one GPU to other GPU and way more time compared to moving the data from one cluster to other. what this means is if we were doing something like 10,000 tokens per second. So there are 000 tokens per second. Fair enough. And my batch is I want to keep numbers simple. So, let us say I'll take my V4 numbers.

The Admin: Let's say we doing 56,000 tokens per second. Fair enough. I have a batch of 32 Fair enough. So, I'm getting something like 1750 56,000 tokens per second each is let's say 8K. So, I'm looking at seven. This is correct. I remember So, this is essentially seven examples going through one single step. Are you clear on this? 56,000 tokens per second. 56,000 divide by 8 which is the B which is the sequence length which is seven examples per second. I'm doing seven examples per second. Are we clear on this? Yes or seven examples per second. But if I now get one more node, I'm going to be spending 2.4 seconds just to communicate between the two clusters.

The Admin: So on one fair enough I can double my batch size now 14 samples per second but I have to wait 4 seconds for back propagation to be calculated. Are we clear on what we just discussed? So it's like you're sitting in Ferrari. you are going out of your house. You have a big huge road. In 0.001 second you're out of your house but after that you are on Bangalore road and then you have to wait in Hibbal and then cross the fly over and then it's raining and then some MPs coming and then it takes all that. So this is why it becomes very important and we talking 27 seconds that is also going to hurt us. So 4 seconds is going to be way bigger when This does not hurt when I'm going to be taking let's say 120 seconds per sample. Right?

The Admin: I'm processing something and that takes 120 second and then I have to wait 2.4 second. So this number is very very important when we discuss how much time I going to spend. For example, if you are spending something like 7.1 second per computation step which is on B 100 and if I'm going to be using 2P over infin which is basically using two clusters I'm going to be spending 2.4 seconds which mean 34% of the time your GPU is sitting idle. It can't do anything. It doesn't even have data to process. Can you see how painful this is? And if you move to B200 and in B200 we take two clusters and our model is small. we are using literally a 1 billion parameter model and we are rushing through in 3.12 seconds and we're spending 2.4 seconds and using two clusters. We're going to be wasting 77% of the GPU. Do you guys realize the problem here?

### 01:20:00

The Admin: What is the point of a 10-minut sigy or zeppto or other delivery if in 10 minutes reaches your apartment but after that he has to log into application he has to send the request to you then the security guard is going to take his Aadhaar number he's going to get a sticker then it's going to go inside the lift and it's going to come up to 18th floor and then who's going to wait in front of your door and deliver it to you. We're going to spend 20 minutes for that only.

Anirudh narla: And I assume you're also going to build for this delay too in the cloud.

The Admin: Of course.

Anirudh narla: I assume you're going to build even for this delay. the 2.4 24 seconds.

The Admin: Of course. Everyone is clear why this is very important.

The Admin: There's one big reason why we went single node and pushed the single node the literally pushed a single node and crushed it and we didn't have access to B200 till the late stages. we had B200 excess that probably would have trained even So a faster GPU raised the ratio of communication to compute. So a volume stays 120GB while the computed height gets shorter. So we don't want that. We want that's why going multiode is a very very complex question and we should not do it unless we if this time is less remember this time is going to hurt so unless we have and this 34% is also very hurtful 34%.

The Admin: So imagine you're paying $10,000 for your GPU compute out of which $3,400 is your GPU not doing anything where it is transferring data right this is like Indian office hours are 8 hours in 8 hours the first half an hour we discuss and chat with people hey what's up traffic weather no salary no money right already does 10 to 10:30 we have our office morning meeting and after 10:30 12:30 we're looking at time. When is my lunch? Then we go out and lunch. Traffic tension problem. Let's have one more time. We go out again, have drink and tea, come back 4 4:30, then 5:30, 5:30.

The Admin: Obviously operationally how much we have worked that's a very very important question when you are paying someone right so please keep in mind how this is going to be super critical for us okay so same thing is shown here so you realize this particular problem let's say we have h00 is going to take 7.1 second for computing something good you have taken two nodes fair enough you are spending 34% of your money on just waiting because you have to share the data

The Admin: between two nodes and someone come Amazon comes to you and say hey B200 slightly cheaper take it you take it but when you take it then you realize you still have to go to the second node so you're actually paying more right this is the economics part of the training of the model and this is why not a lot of people in India are actually training because they do not get this part model and Chinese have Chinese have crushed it Chinese are masters of time management I'm not sure how many of you gone to China but if you go to

The Admin: and the factories the way they work is amazing right so time management is something that they work on but if you are within the GQ then you can see amount of time we are spending right amazing if you have 7.1 second and we using NV link which is within a node just 270 to 7 seconds but if you pan between nodes no okay let's talk about the 0 01 and 02 stages these are but anyways anyone has any question on this

Avnish Midha: Yeah R I was wondering I know Mac Mini provides this Thunderbolt ports right which have 3,000 GB per second kind of speeds. So we can't have a normal blackwell with those kind of ports or something. There's no possibility right.

The Admin: No. moment that's…

MUHAMMED ROSHAN P: So when multiple GPUs are operating in parallel, So when we doing the data transfer, how we are ensuring that everybody in sync, let's say one GPU in half the way and other is complete. So how we'll be ensuring that this synchronization.

The Admin: what we're talking next.

MUHAMMED ROSHAN P: Okay. That's

The Admin: Anyone else? All right. let's talk about So zero is u actually name of a model and we'll talk more about it. Now but let's start from a data paralism. Every GPU holds full 16 bytes of every weight. The copies are identical, Exact same copy. This is the current state that we have. We're not talking about a model split here.

### 01:25:00

The Admin: So 8GPS therefore hold eight identical copies of the 447 GI state which is 3.5 TB of memory just to save 447 billion parameter model. Are we clear on this? We're talking the Old way again to simplify it. Let us say one model takes around 100 GB and we have eight of them. So we have to store 800\. that's all we have done. Are we clear? Yes, hands up. Okay, so old way is same model in all the GPUs because we have to compute the same thing. Okay, and most of that is not needed at eight places if you are smart enough. During the update, each GPU is going to apply the same average. It's going to apply the same loss, same back propagation, same thing is going to happen, right? It's going to provide the same answer. So, seven of the eight are repeating the work, right?

The Admin: If you think about it we can take one GPU and give it all the data that is required and can compute everything and give it back to all other GPUs right some of you were thinking like that but problem is these are nodes these are connected so we can't do that so all the eight have to perform exactly the same steps But the idea is that why don't we give GPU a responsibility of only a part of the model is what that GPU is going to work on right and if we can do that then we can split the model or we can split something we can see what all can be split because the overall stories are required for a model is split between multiple things the actual the 32 floatingoint weights the 16 floatingoint weights for calculations then

The Admin: double the size for the optimized state then my last gradients I have to store all of this right so why don't we split some of these part the massive parts and then across multiple GPUs so we have to move less of we have to not do the exactly same calculation everywhere so each GPU receives a different slice and all GPUs hold the same amount of state and none of them idle so all of them are doing something actually and this is called zero redundancy optimizer this was given by Microsoft oft 2019 to the world and people really took it to next level. Zero is applied in three stages. So we have 02, 03\. The stage one splits the optimizer state. So we have the model actual 32, then we have the gradients, then we have the optimizer states which are for Adam. Now in the stage one, it splits the optimizer state, right? So all the GPUs are holding different layer optimizers.

The Admin: And that is the shard that we're going to be using that word. So each model is going to be holding a shard of the optimizer state in the zero stage in the 01 stage. Are we clear on this? So the GPU has a full model. It has a full original copy of its model. It has the gradients but the optimizer it has only for let's say 1/8 of the model. Are we clear on this? So what all do we have In a single GPU we have the original model 16 floating point which is actually used for computation. Then we have the gradient state for that.

The Admin: And then we have the two optimizer states for atom A1 we'll call that a two states but this is for the whole so if I look at this model and break this model into eight pieces right so let's say our model was 16 layers so two layers then the next two lay the next ers then next two layers then next two layers and next two layers right that's how the model is so optimized states that we we're only going to be saving here for the first only these two states here this part the other GPU is going to save this part so optimizer state because that is also very big right that's how the world started we are optimizing it don't worry don't jump to the conclusion hey I could have done that also people they have Done.

The Admin: already I have to explain a story to you. So here we just splitting the optimized state which is 32 bit weight copy and the two running averages. 12 of the 16 bytes that are required there. So each GPU keeps only one slice and updates only that particular slide. That's all that is happening. The updated slides are then shared across all the GPU. So every GPU has again the same weight that is the state one 0 Here we split the gradient also. So here we're only keeping the original copy of the model in 16 and the gradient are also split now. So optimizer states split the gradients are also split that is a 02 and then we have 03 where the weights themselves are split right. So now each model only saves one it's 1/8 copy of the floating point and 1/8 of the gradients 1/8 of the optimized state. So everything is split in all the 8 GPU.

### 01:30:00

The Admin: This is 03\. If he can work on 03, we can push a massive model on top of our GPU because now the GPU needs to store only a partial part of So data paralism bytes per weight 8 GPUs we have let's say 30 billion parameter model is going to cost something like 447 GPU right this is important in data paralism where each GPU is holding exactly the same data like the model the origin 32 the gradients and the optimized state to be able to do one full and back step we need 2p communication so 447 two are we clear on this this is the data paralism

The Admin: Right? Where the first thing that we learned all gather all reduced this is for the full thing in 01 the weights that are stored on the model is going to be dropped from 447 to 153 but the communication remains same. So we do not lose time in communication. In 02 that drops further down to 104 because now we have shared the gradients also. The communication time does not change. The whole code is written like that. and 03\. You can see that now we have 55 only and the cost here is more. So this is the distinction in all three of them. And here we need to take a call on which one would you like to go ahead Of course you might say that we will go with this. We don't know because we need to test both of them out.

The Admin: 01 02 generally are really good and really 02 you will say that I like to go ahead with where the problem is sometimes the mixture of expert operation doesn't like 02 so we doesn't like 0 01 right so we will want to go on 02 but something like that like the architectures don't favor so we need to because the code is not written by them in such a way but you can See in 03 I can literally drop here something like eight times but I have slightly more communication. So we are slower in 03 but the RAM is now massively available to you. Are we clear on these things? Any question?

The Admin: This is the actual statistics and yeah it's like shad let's take a bus bus is going to be slower compared to shadare only family I sit in the car and then we drive right but sometimes I think in Bangalore buses travel faster than a car for some reason they don't care right okay lman lawman not one one layer two take the model divide by 8 that thank you for raising this question was it Swati was asking me…

lakshmanarao vanimisetti: Like you said slice of a model. Can you elaborate more time on how it's been one layer? Okay. Okay.

The Admin: who was asking me earlier who was I discussing the

The Admin: was the son who was it?

sonu agarwal: So data corruption and then out of memory here and…

The Admin: You are asking that question, Okay,…

sonu agarwal: me and one more person was there ask this. Yeah.

The Admin: thank you for asking the last question. What is a slice? let's talk about slice. Let us say our model has 16 How many layers eGPU has?

The Admin: We have eight GPUs.

lakshmanarao vanimisetti: Take it.

The Admin: We have 16 layers. We have eight GPUs. How many layers each GPU has?

Mukund singh: 2 years.

The Admin: Two. Thank you. Let us say we have 17 because we will make 17\. Because when we make a model, we do not think about how many shards are going to be there in 03\. We will not think about that because we never discuss it. I'm talking V4. Now there are 17\. How many layers are there on each GPU?

Mukund singh: 2.125. Yep.

The Admin: Not possible, right? So, seven GPUs will have two and one GPU will have three. you have to design for this. Got it? I was thinking 1 GPU for me always was somewhere around 4 5 GB higher. Why? Because when we designed a layer, we had 22, right?

The Admin: So in one case we had nine and even if you do that for example even if you decide that I'm going to be taking care of this so I'm always going to make sure that it's divisible by eight the total number of layers we had 22 layers of course you can see that it's going to cause a problem and then let us say we design for that let us say that we conscious that we have eight GPUs and we're going to be dividing our number layers by 8 perfect so let us say we have 24 layers 24 divid by 8 how much is it three.

### 01:35:00

Mukund singh: Three.

The Admin: Now we're going to think, we can use What is Multi token protection. We have MTP1. Let's add MTP2 also.

The Admin: Which means the last layer is slightly bigger. Each layer is not same size also, right? Each layer is different. The first layer if you have big ass en encoding layer that is much bigger and the second is your normal Fair enough. But the last layer, the head is also going to be much bigger. And there you will have this also sitting. Now I think hopefully you will understand that why eGPU will still not be able to hold exactly the same amount of parameters because it's layer dependent and the layers are going to be flowing like this right you can't have half of the part going in because it has to send a state only so layer 1 two fair enough 2 three fair enough 4 fair enough but after that we have this huge prediction so this is going to be causing a problem are we clear and softmax is also going to run on that layer only the slightly more work for our GPU while other GPUs are slightly

The Admin: key idle you clear on this N03 by the way that's why I will see slightly slight differences in the total amount of RAM consumed okay let's see in data data parallelism everyone has everything right in that case we have a 80 GB memory card and there we needed 447 GB of RAM and then we are thinking wow What should I do? that's a question. But you have eight family members. you have your partner, you have your son, you have a small three-year-old daughter. You can ask them to go and work. Why? They're human. They should work. So in 01, what we are going to be doing in 01? This happens. We have the model. We have detected to be state.

The Admin: And each of the model saves only its own atom states. In 02, what do we do further? We also move the gradients on their own GPU. And in 03, we shard the model itself. I believe this is the best widget I've ever made to explain such a complex concept. But because you do not understand importance of zero stages, you're saying

Mukund singh: Does this have a performance trade-off depending on whether we choose 01 02 03 does it impact the performance of the model that is train?

The Admin: performance of the model. No, only the time is taken more for the 03 stage.

Mukund singh: 

Mukund singh: Okay. Okay. Water.

The Admin: I hope you understand 0 1 02 03 04\. I took two years to understand this properly but you're lucky you're getting taught by someone really good. one taught me. Super important in data paralism everything is everywhere. We are spending 44701\. We are not sharing the atom states.

The Admin: Each GPU saves its own atom states. So 01 and 0 is very comfortable, right? But the moment we go to 03, we have all these issues coming in. How much time one GPU is going to be taking, what layer is actually sitting on it, what that particular layer would be doing with respect to the parameters also where the softmax calculate all of those questions are going to start coming in. Nicl that is exactly…

Nikhil Shrimali: Ruben in the zero street stage when the model is sharded across eight GPUs then for the chain rule it still has to wait right okay okay…

The Admin: why we are spending not 2 P time that's the extra P time we have model size can be bigger or…

Nikhil Shrimali: but the advantages is we can train on more data because we have less model Okay.

The Admin: the B size can be much bigger

Nikhil Shrimali: Okay. Thank

The Admin: All right,…

The Admin: it has to go and do one more P. All right, the memory ladder. applying the table that we saw to our own model. Let's say we have a 30GB model that we're discussing. If you're talking pure data parallelism which is by default available in Pythons, we do not need anything special for that. 8 GPUs are going to require 447 GB of overall state. the same 64GB will require the same right that is not going to change in 01 we have 153 02 it 03 drops to 55 if you use 16 GB the amount of data paral is still the same but in 01 this so you have two clusters 03 this drops 0 three it drops further if you go for 64 GPUs which is eight clusters

### 01:40:00

The Admin: This doesn't change exactly the same but this is going to be 117 72 and literally 7 right so you can see the jump from 8 to 64 8 times lower so we can get a bigger node and run run more but again go problem goes back to this part how much compute are we spending on each one of them right because moment we have eight we're talking about this additional 4 seconds that we have to spend. So if the model is big enough such that it takes something like 40 seconds for per batch then makes sense then I'm ready to spend 2.4. But if my step itself finishes in 1 second then spending 2.4 seconds just on data communication between eight nodes doesn't make sense. So it's really a question of money here. You have to literally make a Excel sheet. You have to see how big the model you want to train.

The Admin: then you can think about nodes because then you can short and then you can think that I will push it to such an extreme that each step takes this much then it makes sense to spend around 4 seconds per communication, So something like this. So we have the GPUs of data. This is how If you increase the GPU count, of course, it can hold much more in GPU 1 2 3 right. But if the model size is huge, then even for some till this particular point zero to will never help you right doesn't matter how many GPUs you expand, but at least at this particular point at 32GBs, you can train a 100 billion parameter model. Are we clear on this? Yes or no?

The Admin: Okay.

sonu agarwal: Sorry. I was doing thumbs up by mistake. I did the

The Admin: We are going to be using something called reversibility. I think I'm going to be covering that in next session. And this is what reversibility did for us. This is getting trained on by default 120 billion parameter and by using reversibility we were able to squash it massively. we went to B300 also. So, we would have needed a terabyte of RAM but we were able to fit the whole thing into 2560\. We were slower.

The Admin: you are at least 50% speed but we gained 8x massive speed up and I love reversibility I do not know why people are not using it but we're going to discuss in next session right this is a traditional step traditionally will take around fine 999.6 6GB by the way with all the zeros applied 01 02 03 all of that applied we're not saying that default versus us we're saying apples to apple but using reversibility so instead of 600 GB of RAM we are going to be using something like 125 GB of RAM right now we can go deeper we can make a model bigger you can see here we need a terabyte of RAM this does affect but reversibility is sort of layer independent it

The Admin: Doesn't matter how many layers we add right sequence length it does affect slightly we are crossing the 240 but of course the layer size is not going to be affecting our batch if you increase the batch it increases with that but not as much as this guy if I go here 1 tabyte here you're seeing 10 terabyte so expect at least eight times better performance with the reversibility and half the speed of computation Okay, I am in love with reversal. We'll discuss reversal in the next session. and Offload to CPU is an option. this is something that we can do but we should never do. But worst case, you can do at least for some

The Admin: when we're building the model we do not want computation to happen GPU or we are still processing something we can do it but this is going to be very very slow but we have an option now why we may offload to CPU some computation is because we have a huge model and we want to only run for let's say three four steps and okay we discussed in one of few sessions practically it takes somewhere around 25 minutes for a GPU to start you clear on

The Admin: I'm saying the worst case a good day it will start in somewhere around 10 minutes you need to spend at least 10 minutes to start a new cluster it's going to boot up it's going to download a model you can see image and everything I've downloaded do whatever you want right you're going to be using a specific library of triton kernel you will be using a specific pytor you'll be using this specific that it will take around 10 minutes for the GPU cluster to start processing and you would spend money So sometimes you will want to offload to CPU because cheaper everything is there it takes less amount of cost of course it's going to run very very slow but it's okay for some test to do right so we can offload to CPU NVME is something where we're basically using a data from the storage

### 01:45:00

Anirudh narla: So, how does this offload to CPU work when you're using the cloud GPU essentially?

The Admin: Did I show you the cluster for B200? did it mention Intel? Were you noticing?

Anirudh narla: Yeah, I didn't. I'm sorry.

The Admin: Okay, Swati.

Swati Bansal: Yeah I don't know if this question makes sense but till now we have been talking for all these algorithms from the perspective of just model weights right…

Swati Bansal: but we also have tensors for data we have the checkpoint data and all which takes memory but why are we not accounting for that is it because it doesn't stay in the RAM

The Admin: because we no…

The Admin: what we do is when we're training again based on the cost we're going to decide after how many steps we going to be taking a checkpoint so when the checkpoint happens GPU has to stop so we are going to spend something like 1 minute

The Admin: to move the model from to CPU. the architecture we followed was and it's again very important because we failed miserably multiple times to get it right and we did get right finally but we lost a lot of checkpoints because of that. Now let us say our model is sharded between multiple GPU your whole GPU is there right so it is running for thousand steps why thousand steps because that's something like $100 or something or $200 $500 for us for example so we market it like that once that happens after every I think 6 hours or something the model stops for a minute the whole data moves to the CPU in chunks only and the GPU starts again now the CPU is super busy CPU needs to look at this 1.2

The Admin: because we have to save the atom states and checkpoint is not just everything checkpoint is that checkpoint is 32 copy…

The Admin: then the gradient copy checkpoint is the optimizer state and everything so all of this is going to be combined in the that we have big CPU that we have and the CPU has to have around 1.2 teraby of RAM otherwise this can't happen but GPU is busy by the way it just waited for a minute or two and then started starting from scratch when we ask AWS to give us a cluster it gives us a cluster and…

Swati Bansal: Got it.

Swati Bansal: But you said that the start time is more than 10 minutes. So it's not okay. Got this.

The Admin: then we install all the libraries all the Titon kernels all the versions of the correct thing exact Python that we need so that part is around

The Admin: 10 minutes data getting downloaded from S3 old checkpoint getting downloaded because we don't start a new model right we start from the checkpoint that is there so we need to download checkpoint we need to download the pytor we download all the right libraries we have to install them we have to make sure that the installation is correct after all of the check is done parally data is getting downloaded and we did a mistake of downloading data serially then we realized on a kernel zeon CPU so we massively launched thousand threats for data download so what it used to take around 10 minutes to download

The Admin: now takes around 2 minutes to download right so there are all of those things that are going to come into picture so once the data is there our checkpoint is there from other S3 bucket then the training starts now when this happens parallely also what has to happen this has to upload it to S3 so all correct so all installation data movement combination of data saving statistics we'll have a server also we're going

Swati Bansal: …

Swati Bansal: what you're saying is all this is happening on CPU and not the GPU. That's where the data. Okay. Right.

The Admin: received a training statistics where is a loss where is a gradient all that is happening that is yes and…

Swati Bansal: The ledger and all that is living on. Okay. Thank you.

The Admin: both are important because if this guy hangs this guy then you're gone yes as I shared earlier the 200 and…

Swati Bansal: So, do we have a CPU cluster at the same time?

The Admin: specification we saw it gives us both we are going to get this 2 terb of RAM and…

Swati Bansal: Okay, cool.

The Admin: if you go for let's look at G DN. Okay. E6 E6 E

### 01:50:00

The Admin: Yes. P6B00 lost this one.

The Admin: So we get 192 virtual CPUs 4 TB of RAM and Intel zeon this is the one that we have we always get same we always get a combination there's no way you can just get a GPU can't use it all right…

Swati Bansal: So that's a combination of GPUs and…

Swati Bansal: the CPUs combined which is kind of Thank you.

The Admin: then we have FSDP and deep speed. you just need to know about them. these are the two libraries that are there. A deep speed is a library that Microsoft released alongside with the zero paper. It's a simple configuration file. Everything is going to be installed the back end. In that configuration file, we're going to be seeing what do we set up. So now let's go to chargit. Can you make one example juice on for

The Admin: 0 0 1 2 and 3\. Yes. So how it's going to look like. That's all we need to do. So from our side we need to say a train microbat size. We're going to say 64\. Then we're going to say train microbat size per GPU 4\. Right? So we have basically let's say 8 GPUs per Each cluster we are saying can you send four batch to it and we're saying we have two acclimation steps. So that makes 64\. That's how we make this is the only file that we need to make. Then we say FP16 enabled Then we say optimization one. So here we're going to write 1 2 3 4\.

The Admin: Which state do we want? Then we're going to say which optimizer we want and R for The BS for the APS for the VK for that. So that's the 01 stage, right? Optimizer states are shared in the 0 same thing here. Optimizer state zero. Overlap communication true continuous gradient true reduce scatter So these are things that we need to mention. Optimizer is saved and then the gradients are saved Then in the 03 we are sharing the model also. So first two are same. Here we're saying three overlap communication control gradient reduce scatter safety prefresh bucket size based how much of the

The Admin: additional storage I should keep for the data to come in from the other GPU right so then you specify more of these things so it's litally something like this so 01 parameters all gradient all optimizer are sharded in 02 parameters all gradients are sharded and optimizer sharded in 03 the parameter sharded the gradients are sharded and optimizer sharded so when we have a shard once the training is done and you save a checkpoint the shard needs to go on the CPU and the combination needs to happen or the conversion of shard to a single file needs to happen on the GPU

The Admin: and then we upload it to S3. So all of that work is done by deep speed and FSDB2 which is fully sharded data parallel. So the deep speed part handles the computation and other stuff and FSDP handles the sharding process and the stage three requirement of basically making sure that the model is shared properly. But they're already built into Python. We don't need to worry about it. You just need to know because when you're installing it, it will claim cry FSDP version this, deep feed version that. So you need to know what these things are. overlapping communication with the compute. section five we discussed that this is a very important part overlapping communication with compute. when the computation happening on the GPU some communication should also happen between the GPU and other GPU.

The Admin: So if we can paralyze that then we get further speed ups. This is already done in deep speed and FSDP but we need to know what exactly we're discussing. A simplest way of that is to understand something like this. on the compute side let us say we have 1 2 3 4 5 6 here So if you're seeing we are looking at the bucket site. What exactly is a bucket size? one training step on a pin 10-second axis we are looking at overall 10 seconds of computation. Here we can be looking at H00 or H200 is going to be faster. This is going to be slightly slower. So let's stick to H 100 Here we have two layers We have one layer that is a bucket size. Right? What is there on each of the GPU essentially now let us say we have something like Everything is there on one single GPU. Then we compute everything on one GPU then waste time on communication.

### 01:55:00

The Admin: But if we were to parallelize that, if we make a bucket small, then as the GPU start compute for the next step, it can be using the network to communicate. Are you clear on this? This is what we want. So look at The amount of time it takes to compute them is the same. The L1 is going to stop here. But if I increase this, you're going to see the communication takes longer and longer and longer. That is the reason we want to go as small as possible for each bucket. And this is even worse in B200. This is a crime. We should not be doing this as small bucket as possible. But here you can see the communication is slightly overlapping because we picked a model that takes less time compared

The Admin: to the communication that is required. So training a small model on B200 is bad. Are we clear on this? Yes or precision and what Blackwell changed. Then came Blackwell. All of the world was thinking okay I have to spend that. And certainly Blackwell If Blackwell wasn't there, we will not see Astra, we will not see Fable, we will not see Opus 4.7, we will not see these. Nvidia is actually playing a big role in all of this. Now Blackwell came in and they said that now they have maximized the FP8 computation. they released their own paper. They proved to the world that you can compute in FP8 let alone BF16 or FP16. Now you can compute in FP8. And when you compute in FP8, this thing happen.

The Admin: First of all, the bytes per weight is 16 here. When we use 8 bit weights in gradient, we're going to be spending something like 14\. So, we have some saving there. And 30B model was taking something like 447\. But it's going to be saving some size there also. But that's not the point. Overall reduction is only 121% here. But that was not The actual gain was in the processing speed. the TOSS Titan reports training up to 41% faster. Are we clear on this? So if we train on FP8 of course we are going to save some RAM also because the sizes are smaller but the biggest gain comes in and okay why don't you see eight here anyone why is this not 220 and while this is not eight gradients

Syed Abdul: The gradients are 16\. So the average is 16\.

chirag Tagadiya: The final gradients are in 16 plotting point but the calculation happened in eight.

The Admin: And we still have to store the 32B original copy of the model and…

The Admin: the optimized states are also in higher precision. So we can't move those Add W8 version is There we can save slightly more. But the main reason we don't see a half of this is because not everything can be stored in FP8. Computation will happen in FB8. So whatever matrix multiplication or the weights that I'm saving that can happen but 32-bit original copy has to be there. The optimized states have to be there. The gradients have to be there. Grad you can go to FP16 BF16 not slower than that. So only a small storage space is saved but maximum gain comes from really around 40% speed up. So now I can train even faster.

The Admin: So on the prison side we have FP BF16 and then we have FP8. You can see that this is the size different. Then we have Adam can move to BF16. causes a bit of loss in accuracy. But if you move to FP8 and BF16, you can see overalls how much amount of memory you can save. Are we clear on this? Right. BF16, I want you to look at this and the bottom table. So shared states are less peak permutation table 100% activation by 50% less, commigation by 50% less. If you go to FP8, nothing changes there. If I move the atom states, then that changes. Clear?

The Admin: So what did we run? So in our case we ran BF2. We were many stages. so this is just a particular stage of the model because we We ran 0 0 1 02\. We were using BF16. the sequences per GPU were two. Equation steps were two. I think this is a complete last stage. Glob 32 which is also a Peak learning grade went to 3 e minus 4 weight decay is zero. We cannot use weight decay with reversibility. We'll discuss that next session. Gradipping was one and the bucket size was 2 E8. The same bucket size saw this The sharding we have to figure out what are these bucket sizes, right? We have to calculate a lot of money is spent by the way just to get the bright this file.

### 02:00:00

The Admin: Just to get this file right, we have to spend a lot of money. Do you realize that? can you share my pain when I say this? We have to run with multiple configurations and then see how much or still we can push more. And it's not that sometimes we have a leakage, right? And in that leakage we see that okay my model fit as we're training moments as we're training it further we are going to see some leakage because some file some sharding or while some communication between the GPU something is not deleted. So you're using let's say 120GB you're happy but you can't say that 80 is going to stay constant. You have to train it for some at least 100 steps when you train you're going to see that slowly increasing that this state is gone at work again.

The Admin: lot of at least a week is spend just to get this state correct that's why it's a expensive deal now what are the v5 decision that we have to take what you have to figure out is that are we going to be using 01 or 02 or 03 because based on the model size we need to figure that particular part out second is if you're starting from 02 then are we going to go for sharding and what is the size of that and then the next question we need to answer is what is of size of model that we're going to be training. remember the inter GPU communication that is also there right so we have questions on 02 then we have how many GPUs per node then we need to figure out are we on FP8 I'm getting confident that we should train on FP8 this time we

The Admin: have Blackwell also means that model size can be big to start with. Also earlier we had two billion parameter then five then nine and then 120 billion parameter model that we train in the growing sequence. This time that sequence can be bigger. So we can start with a bigger model and then end bigger. But that also brings a question that are we confident on the model architecture or we still start small. So those questions are still there to be answered. And does any state go to the system memory where are we locked? Are we going to be communication bound or we're going to be compute bound? All right. Any question?

The Admin: Anyone any question? All right. If no, then your assignment is Work with the agent and create a simple 32 virtual GPUs. you can easily do it on your own computer. It's a small program that works can be the GPU on the collab also. Then write a demo model that runs on top of these 32 virtual GPUs. Simulate 01 02 03 and show how the memory and computation changes anyways your cloud is going to do it. But I want you to see the results yourself. I want you to see those results and ask it to make sure that it matches what zero does.

The Admin: submit your IPYB notebook and your GitHub rep and explain in detail that you do understand zero stages and you understand the pros and cons of each of the state that you have. That's a simple assignment. question at All right.

The Admin: If no question then I'm going to stop the recording

### Meeting ended after 02:05:05 👋

*This editable transcript was computer generated and might contain errors. People can also change the text after it was created.*

