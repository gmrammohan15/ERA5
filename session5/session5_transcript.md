## **ERA V5 Session \- 2026/07/25 06:37 IST \- Transcript**

# **Transcript**

Vardhan Walavalkar: happy word

Soma Korada: Happy birthday, Rohan.

Yasir Reshi: Happy birthday.

rammohan madhusudan: Happy

Kunal Sinha: Happy birthday, Ron.

The Admin: Thank you.

Avnish Midha: Okay.

The Admin: Thank you.

Satyanarayana Murthy Toleti: Happy birthday, sir.

The Admin: Thank you. And same to you That is my comeback on happy birthday. If someone wishes happy birthday, I wish them the Happy birthday to you also. All right. So, today's session is maybe interesting, but this is the foundation session. In fact, someone just shared on our chat 5 is launched right nally 9 years ago.

Soma Korada: Bonsai model.

The Admin: 9 hours ago and if you see how we compare these models is that here we are saying agentic terminal coding we have 43.3% table 33.7 opus and these are the benchmarks that we saw them in the last session also but these are benchmark which really tell how good or bad the model are and it's not that you train a model and then you run a benchmark and then you realize the model is good on this particular benchmark that's not The cycle is to find these targets first and each one of them has a different expressivity of intelligence or what the model wants to do. That way we need to define the training set that you have done also.

The Admin: But there also the problem is that how do we define what do we train on and that's where most of the trick is that's where most of the challenges are because that recipe is something that is not shared definitely but we can sort of reverse engineer that through the research papers that are there and some of the things that people comment on. So that is what today's session is about data mixtures and the curriculum part right. So till now if we look at what has happened in the first session we got overview believe me transformers are coming back it's not that all the sessions are on data but I just want you to understand this is it like if we get this right everything else is very easy because model architectures are sort of fixed we can add some improvements with respect to how much memory they're consuming and how fast they are and how big they are but this is the core of every single

The Admin: model that is being trained. Till now we understood the slow and unambiguous work. Now it should be unamiguous. How do we filter it out? How tokenizer and data set are sort of linked? We need to have a partial tokenizer before we can even build a data set. And after we build a data set, we need to finish the tokenizer. So there also is a cycle. And then we looked at the cleaning and dduplication and a Provenence would mean that I know where the data is coming from and there's a guaranteed check on that also. So we did all of that. Today session is all about once the data is clean and ready for us what is a training plan? How do we feed that data to the model? part comes What part comes later on?

The Admin: And even after we clean the data there's going to be super premium highquality data that we need to preserve for any linking stage. We're going to discuss that part today. That is when the model actually shines that is a PhD level of training for the model where only the best examples are shared because you can't share a bad example at that time but the point is at that time the model is ready to absorb everything. It's like the young Einstein waiting to write the relativity paper. and that is where the data mixture part will come in. How do we mix different kind of data sets at different stages to slowly explore and exploit the model behavior.

The Admin: Initially I just wanted to show you this thing which is let's say we go to category and here we ask a specific question what are some of the special properties of number 17 for example Charity thinks a lot these days. The prime number divisible only by 1\. 17 twin prime forms with 17 and 19\.

The Admin: Forat prime 2^ 2 \+ 1 one of the only fine known format primes constructible polygon a regular 17 polygon can be constructed exactly using the compass and so on and so on right now where do you think this kind of data will reside where is it source of these kind of where information that is one question to you like and here I can ask also this is something that I

### 00:05:00

The Admin: was reading about yesterday that's a conflicting yeah even if you just stick with this what do you think this information you can think of it stays in Wikipedia but what do we call Wikipedia then is a general web or is Wikipedia going to be a scientific journal or if it is knowledge fact then everything that is documented will be there. But there a lot of things that are not documented.

The Admin: Where are these information going to be from? then you can ask who or which. Right. In fact, there's another weird question. can you find the names of famous

The Admin: people who were born when the mothers were more than 40 year old right this kind of question for example here it came back he's asking okay I've seen the question now here where do you think this information is going to be anyone this kind of information I'm sure that you'll not find a Wikipedia page for this or can you find a name of famous people who were born when their mothers were more than 40 years old and the mother was also born in July right now? anyone has any answer on this? Where do you think this kind of information is?

Suyash Patel: I imagine on general web, but then you need to do some processing to to

The Admin: Here it's doing the agent call.

Yasir Reshi: I think it's in different sources.

Yasir Reshi: So, it's picking from different sources, collaborating putting it together, and throwing it on us.

The Admin: But if I were to just say don't do agent call and tell me what we remember. So in that case Where the information will be stored for the model to learn something like this social media.

Madhu Charan: The gossip

Arpan Das: Celebrity gossip magazine.

Soma Korada: social media.

Soma Korada: I'm not

The Admin: all of you are basically seeing web right now when we discussed today and in fact in the last session also we have this question of why so much of web because the problem is that all of these weird information is on the web there is no source like Wikipedia and big company anthropic and open they have definitely distilled every single knowledge based property so they can train out in the easiest possible way but for us and other people who have not done it we need to rely on the web where most of this kind of information is there right we'll come back on this and you'll find one of the

The Admin: very very famous people are listed here. So that is the data mixture part. and the question we ask we are answering which you will have is that why a big part of the data set is still going to be web even though it doesn't make sense because when we look at the benchmarks when we look at the data set you'll see that a slight mismatch but we will try and dig in that particular part also right and our target is clear our target is coding and agentic work. here also if you see it is doing What is agentic work? Where you have a question, you don't know the answer or the question does want you to use some tools. So, you need to know how to use the tools. that means that every single clot session

The Admin: or cursor session that you have done till now all that is training data somehow if you can share it with the model can learn better but there also we need to understand that what is it that we actually okay two parts and this is an important distinction it will come later again but I just want to make sure that I don't forget it to explain this part to you let us say user is asking very simple question what is the capital of India? And the agent let's call that agent only responds back very simple new Delhi.

The Admin: If this is a pre-training objective then question to you is the loss calculated on if you think all words then raise your hand. If you think full words then show thumbs down. This is all Right in the pre- training objective, it is going to be every single word. But in the agentic process or if you're doing the post- training part, we are only going to be training on this New Delhi.

### 00:10:00

The Admin: And that distinction is very important because now if I just switch this let's say we have a user asking question then agent then that is responding then we have a user that is asking question then a agent that is responding then we have a user asking a question then we have a agent responding agent has called a tool it knows what tool to call there are lot of tool data that comes in and then this data goes back to agent agent decides something again and then we have finally a user who's giving the feedback. we have 1 2 3 4 5 6 7 8 and 9\. First of all this kind of data we don't use for Pre-training is Wikipedia and the news articles and where it has to go through because this is waste of the resource at that time.

The Admin: This kind of data is used when we are finally fine-tuning the model where not even fine-tuning it's much before that but we're talking about when we are training the model to become an agentic model. Now in that case the model is going to send all the text it has to predict something but the loss is calculated only on 2 4 6 9 I wanted to answer do we put the seven in the loss or not. Seven is the tool telling the model back that this is what happened. And I use this command and my

The Admin: I wrote a loop or the net excess was given and the logs that you see when you run. do you think the seventh is a part of the loss or…

Suyash Patel: No.

The Admin: not right show loss difference.

chirag Tagadiya: I think it depends if it is a thinking model you want to show the thinking process then. Hot.

The Admin: So yes or no loss is there or not for this?

Satyanarayana Murthy Toleti: No.

The Admin: Loss is not there for So you need to have all of this distinction.

The Admin: If some of you don't understand what is this loss you're talking about don't worry we're going to capture that also but the point I'm trying to make that even the data set might look very big in the later stages some part of that is trainable some part of that we will just view the data set but we will not try and predict what the model is saying because the tool result can be anything when you launch an application there's no point training the model on what that log is we'll send the log to the model so it can

The Admin: look at the log and say this thing or this tool failed because of this particular issue right another simple example for example there's let's say FMPG or MPG tool that's there which is used for making working with videos right it can allow us to edit videos and so on let us say agent said hey ffmpeg open this video which is m og

The Admin: Let me show that. that may also exist. Why not do a Maggie? let's do a file called 4.m maggi and change the FPS or remove the last 25 frames. Let's say this kind of command is there, And we run this command actually in the environment and the log comes back and say that A G is not supported. We will not be training on this but we'll sending it to the model can look at it and say it's not there. So you can ask the user that your format is wrong right it can remember that Maggie is not a format to be to run on ffmpeg. So you can make those distinction.

The Admin: So where we are going with this is as we continue to train you're going to realize that okay here we have some interesting people Susan Bole Charles Darin Stephen Kovitz Selen and others right and that's where the data mixture comes in everything that we collect is not put into the loss again what is loss is whether we are telling whether we're punishing the model for not predicting a particular token right so now That should make sense. We should not punish the model for predicting what any random tool can give us as an So when I run my application, for example, this camera application, something I only build. Now when I run this, I get this kind of log.

The Admin: There's no point training on all of this. We'll send to the model to understand if I launch this, What all can we launch? What is the kind of data that comes back? But we'll not be training on it. It's very important and this this will get crystallized as we discuss more today. The point is that we need to have Based on a training plan, we are going to decide on the data mixture when what kind of data we are going to be mixing at at each time what category is the model going to see. For example, we discussed this agent trace. This is exactly the data you guys are creating right now.

### 00:15:00

The Admin: which is your widget creation and talking netifier you did something your port was logged right what's the point of training the model on a data where it says your port was locked but it is important to see because model can see the port was logged this is what I should have done so model will think okay the port was locked I'll try and use another port instead of that if it comes back to you and say that port is log I can't do anything then we log submit the loss right now how often it see the particular kind of data at what stage the training it's going to be seen.

The Admin: the clean corpus and the same compute budget can provide completely different kind of models depending on when exactly are you feeding it right because if you feed the high quality data which is on PhD level agentic traces and function calling and latex and clear python scope or clear python books very initial to the model when model doesn't know when the model saying abad and it is just going to consume without learning anything. So we have to have a very clear idea of what part of the data we're going to be feeding and if that is done properly after the data is clean then you guys are at a very very good model. Now the target is clear and this is something that you and I need to align at because you guys are going to be creating clearing data sets and allow us to make this model. Our model needs to be really really good at coding at the agentic task. Right?

The Admin: When we say agent task, you saw what that ceiling on is asentic. When you ask a question, today models are very clear that I don't know the I'll go on online. Where do I Important question, What part of the search should I show? All those questions is what makes even a good Today, chatbot is not that you ask question, it responds back. Every time you're going to be asking something, it goes online for a good deep research and comes back and distills information, gives it to you. So without coding and agentic you can't have any model that is useful. You can't come back and say that I can make a financial model. What does it mean? Financial model would mean that you again have to have a tool calling capability. It can call accelerated tools or max and min and mode and averages and average off with banking order right off in the banking format. So there are a lot of things that a model need to know and for that it needs to be able

The Admin: able to use the functions or tools or calculations. Now you should be able to do a very long task. That is something that is an additional objective for us which is what you see when nowadays it's getting less. But if you were using coding tools in 24 and 25 25 then you will see that a model after some time it start behaving that today's Friday evening I'm going it will just not respond right sometimes the chart will just end sometime charg just not load and continue because the long horizon task were very difficult and this is where the gold data this is literally where the anti- matter data is there and labs are preserving it if somehow we can collect this data then

The Admin: you again model can beat things and same thing here if you look at the P that I opened earlier open focus 5 patient equivalent bench right now cost per attempt this is basically long horizon part first of all these tasks are difficult but how long does it take to actually solve a particular task here you see that performance goes from 35% to 45% where the cost goes for $5 to $20, right? So this is something that needs to be fixed.

The Admin: This is something that you have arc again agi kind of problems where opus is very low but here we have opus 5 again very high but the cost we'll see is $20,000 for solving this benchmark if you were to even take part in this benchmark that's some amount of money we'll have to spend way more because this is the deployed opus cost which is way less if you were to do this on the test level or where the model is getting trained on the big H200 probably will have to spend $100,000 just on So all of these evaluation essentially humanity's last exam example here again you're seeing more cost being spent but the point is that you can actually make an end toend application. This is an example of what 5 built. Yeah, this is a working example. So we can open it and check it out. So here you can see that this whole application is built by one chatbot, one single prompt.

### 00:20:00

The Admin: So You need to keep on keep on checking things. You need to know how to check things and what kind of u data might be required for the user interact with. How does the UI look like? All of that information needs to go in. That is why this long horizon is one of the I'll say mecca of things because you can put an AI which or agent or model in our case to be able to continue to think and continue to improve and continue to solve its own mistakes. we essentially are solving…

lakshmanarao vanimisetti: That's you.

The Admin: what India doesn't have as a country right okay target is clear for us the coding and the agentic work is the utmost importance it should be able to take a long task plan the work call tools

The Admin: across multiple steps. Read the results. Then recover the call fails and continue. And this is exactly where I was talking about. here you'll see that we are saying recover Recover when a call fails. The model did something for example launch a particular function or call a function in a wrong way or write a wrong code. The compiler fails or the Python error comes in and based on the error nor the model does something new. So while training that error we do not train on we will send it to the model so model can see what the error was but we are not going to train the model to become Python training on the error log would mean that the model can think or can work like a Python compiler which is a nonsense which is we don't need that you can decide to make a model for that purpose only but or how a tool looks like and writing that error exactly in the same way is not required right for example

The Admin: when you do something something crashes it crashed you can look at the important information and then proceed for example if this browser crashed or this website crashed you'll get error log you'll know that okay this particular command didn't work or it couldn't read that particular point from data set that's the only important part rest all the logs that are there that this was a time this was a javascript version you're using this these are the other applications or other extension that all the information is nonsense so that's why we don't train on it it's going to be waste of time but this is the objective so if ever now you're thinking of what kind of model we are planning. the target is clear coding and agentic need to be good at indicy assistant which is able to take a long task plan the work call the tools across multiple steps read the results recover when the call fails and continue operating while holding the growth growing history of the task in context. So that's the objective of the trend model we are targeting. We also want whose depth of reasoning can be controlled. This is very very important.

The Admin: Everywhere you would have seen that how deep you want the model to go. You think You wanted to think very high number of tokens and that is something that you have to train on. Have you thought about it? how do you get the medium hard and super and ultra thinking performance? The model has to be trained on. You can't just say I'll just use the first 500 token and call it medium. I will just use the 5,000 tokens and I'll just Think more. That is not it That's how it started but that's not the state-of-the-art. you have to hint the model that I wanted to think more. Example this is my favorite interview question. Whenever I hire people they're explaining I ask them talk about yourself they're talking about the date blah blah blah. Then immediately I stop them and ask what is 43 divid by 17\. Can you guys answer that 5 seconds?

The Admin: 1 2 so we don't have time to open app and now 43 divide by 17 if you think 17 into 34 34 and then I said 17 half is going to be 18 so 9 then we said 34 \+ 9 then you can calculate mean 34 \+ 9 there's a 40\. 34 right so answer should be close to that 2.5ish kind of number so that's a short way of thinking that that is where we want the model to be so we are going to h the model and model needs to tell us immediately what it thinks then we need to provide another token which tells the model it can think more then we provide another token that tells the model to think high which means you have to have a data set for that so now whenever you see claude or charge or others giving you free

The Admin: things that is you making the model for them. Have you came across that you are answering an experimental feature? Yes. Which answer to which response do you like? Yes or no? That is the exact training data set that you are helping the models to create. Right. So this depth control let's again look at chargeability. So this high, medium and instant these are the pointers that go to the model where the model is told that okay you need to we don't have a charge GPT 5.5 high or medium or instant right those 5.5 in might be there but when you're coding definitely these are the traces in fact codeex I don't know here I have my here I don't okay so if you're using plot

### 00:25:00

The Admin: code. You'll see there you in fact have full car. I don't know what else should I call it. Looks like a car to me. The kind of features they've added now, right? You have full slider. This is you putting a break. This is you burning the so many different levels. So this is something that the model has to be trained with. So again the question goes back where is this data set who has the data set where we have a tag for small less think more right so that is again why I keep saying data data so when we say we also want a strong reasoning model whose depth of reasoning can be controlled simple problems should require little thinking while difficult programs should require more thinking and in greater depth so there needs to be the process or

The Admin: steps stored somewhere where we have an example of model thinking short and then use a model for training that and the answer also has to be good or goodish right and finally model must understand and generating indicatively that is the primary differentiator that we have so it should be good in we basically making Indian right that is all Indians are where you can speak an Indian language and you are intelligent you can be hired by Google all of companies outside India and then he can basically settle. Do you think this is how Indians work? Are we not defining an Indian? This is how I see most of people joining.

The Admin: or the CEOs of other companies are right. why the mixture is the model? This is again something and this is the key I want to take out. This is one statement that I wanted to remember today and take it out because in future if you are in lab and you're training your own model that is the definition of what the model actually is. So the easiest way to understand the mixture is a real design decision and that decision once you take the setting the DNA of the model and you'll see the model behavior changing also as we start changing the data set as the model is getting trained. Now if more of the fixed token budget is allocated to code and less the generated web the model become definitely good at programming but it will have less world knowledge. Right?

The Admin: So what happens is a model is really good in programming and it can program anything that you want but the moment it has to use common sense that common sense is not there right so now if you say write a model to count the number index finger numbers on humans and you'll be given how many humans are there in the room if you don't have common sense you will write a program that okay ask the user how many humans are there in the room and give me a list of index finger of all humans because one may have two index fingers, human may have four index fingers and so on because common sense is not there. So that reasoning that the understanding how the world works that animal has four legs, human has two, right? Or the IQ of man is 80 and woman is 400, right?

The Admin: All of that common sense information it has to be learned on, you can't just assume that it's there somewhere. So you can make a model that is really good in coding. The code won't crash, but the code just doesn't work because the common sense information is not there, right? Or for example, book You can't book a ticket for me at 2 a.m. It needs to be sometime I can go or at least ask. So those things that are there, I will write a letter to my manager that I'm not tomorrow and I will not come tomorrow. So you can't expect the model to write hey I think I will not be tomorrow so I will not come tomorrow. You want to detail some GAN and other stuff needs to be there right. and if a fix share is reserved for indic language the capability remains protective.

The Admin: So that is also something we need to understand and today we'll see why in our case especially that we need to have this additional capability preserved without the protection English is just going to destroy because there's so much of English content out there that we just can't match that. Now the total token budget is fixed. So every additional step is going to be designed in a way that it can give some superpowers to our model and build on top of that. So here we have a mixture composure. I want us to read this mixture is a capacity decision composer baked into the benchmark. So the data that we have here is coming from the benchmarks that you guys also selected as a part of the assignment. This is the main pre-training run and it is general web heavy as you can see that here we have general web is around 34%.

### 00:30:00

The Admin: And because it is the most abandoned data, if you move the sliders here and all, you will see that things are going to change. but what I do want you to read is the last line. The scar lanes agentic and verified in indic and long reasoning are held small on purpose and the concentration concentrated later in the short and lean phase. So this is not the first data set from a training perspective.

The Admin: We talking to college level for a model. This is not a The school level is going to be a lot of your general web. So we'll start with the general web and as we are training and as the model is reaching that college or PhD level this is how a data set will look like. This is let's say 100 samples 34 of that will be web 12 of STEM is your science technology. 16 is going to be agent tool calls. Then we have long context also getting in slowly. We have reasoning traces also coming in. Then if you have code right and this is set of 100\. So if you move one you're going to see that you have to change others. So when our model is in the college what college you want him to go the model is going to go in a MBA college or it's going to go in engineering college or it's going to go into a arts college and so on and this is the behavior you are setting in.

The Admin: So as we train a model we have a lot of data to cover through once we are somewhere around 80% data this is how the data will look like we clear on this part this is not the first batch is going to be abd as our model is coming to the closure of the training part how our model is going to look like right now here we can decide the model is going to be super clean on indic everything is indicated as well but if you just do all of that this is how the mind is changing here it is becoming a exactly. Here it's a BJP spokesperson should Hindi and hindutwa only that logic but right and if you just train on long context and nothing on else now here we have shashi who can answer a question in 4,000 words where people won't not understand. Here we have reasoning traces right here we have agentic where it just gives a command.

The Admin: So here here if you train a model on agentic and code only for example and you push for code only and agentic right somewhere over here. Here if somebody asks that why are you not putting them in the prahan or whatever the demands are into jail or why are you not asking him to design the model is going to think think a lot and think a lot and come back and say 42 because you have only trained on code and agent authentic and it has no idea how to answer you've taken away that cap capacity. So this is something that we need to be aware of. How you decide the bucket size? How you decide what is the part of how much of the training set at that time is code or agent reasoning or freezing traces or long context will determine how good the model is. Very very important phase. You need to think of model literally like a small child.

The Admin: You're a child you're training in initial part has access to everything. earlier I at least could say that okay we should think about how I was taught third class and I thought of that will actually work also but I'm seeing the modern generation the modern kids are taught everything. They have a mobile phone and they know every damn thing that is possible. So I didn't have access to that. So that's not how I think the behavior changes. So where I'm coming from does it make sense to even tell about quantum physics a black hole to a 4old and answer sounds like yes because today's kid can handle that they know the black hole exist and star wars these kind of things have taken place and interstell the depth of knowledge of each topic is different right which concept introduce when is not the question how deep shall we take that particular model

The Admin: In that concept is the question right that is where we need to think not that we'll not even talk about things that the kids are not supposed to know the model will know everything but the depth is going to be slowly increasing so there's something that has to be this is not decided that's why this is a slider and there's no reset so you need to help me part assignment also you need to think hard and tell me that you think that is going to be right now as you move this data set right you're going to see that this also changes so you can't

The Admin: think that okay I'm going to make a model that is super in writing any Indian language or conversing in any Indian language go ahead but there is no data set right't we need around two trillion tokens here where will you get them right so not possible so there are things that are going to limit us based on the data availability here we need repetition we are already repeating our data set here we are sort of covered Right. So it's not that you'll just think that you want to train and you have the data set. So again again restriction comes in. Now as changes also you're going to see that these benchmarks also change that is also linked. So if you don't train on code enough then you will not be able to target the benchmarks So reasoning traces need to be there for getting the reasoning and stem long context need to be there for the long eval to come.

### 00:35:00

The Admin: But if you keep all of them to 20 blah blah blah blah then we have reduced our general web so much that we will now fail at MMLU is under whenever you see MMLU is basically a GK. what is it called? What exams IPS officers?

AJ Jain: You'll be

Soma Korada: Stibles.

Tejaskumar Reddy J: your PSK.

The Admin: Yeah, MLM is Basically whenever you see UPSC you ask everything every damn thing. So it's literally that kind of data set. So this has to be designed very well right and now think about it.

The Admin: So you and me sit together. We define the best transformer architecture that here the script connection will go from here to here. We'll have the modern optimizer. we'll use flash attention 47 not invented yet and we do everything possible. We write a beautiful tokenizer and this data set is not there and you have not trained on the data set. We forget. We just say we'll put in a data set in a folder. We'll take a model. We ask the model go look at the folder and train it. you will get crap.

The Admin: you will get I don't want to say but Rahul Gandhi and we will get things that you don't want right it's not that the other side is good everyone is gray right now looking at what is happening so it's like I can put everyone in same bucket today that's how things evolve but point is that you want someone like Dhoni for example right maybe yes right so if you want a sports person like him or if you want some intelligent people I'm falling short of people who I can call intelligent who have not screwed up even in that list but you get the

The Admin: point right you want really really smart intelligent people if you want that then this has to be decided we have to make sure that we know what is it that we're training the model on and at what time so what today's session is all about what time okay we'll hold for a question here now before I do this is how native heavy looks like this is sort of the initial one right this is how our data set might look in the middle phases because you can see coding is also expanding but the web is going to be a generic full context question which is going to be going.

The Admin: This is how most the analing part of the pre-training will look like and close to the analing it's going to become something like So you can play around. This is my thought process. I do not have any scientific backing for This widget was made using going through lot of papers and seeing what a lot of people are doing. A good way to become smart is to see what smart people do or a good way to train a model's curriculum is to see what other people are using in the curriculum. So that is how I built it. So now we open for a few questions and we have AJ AJ.

AJ Jain: Yeah thanks so don't first of all I think this visual is very very good to give that intuition the question is and probably you answer it the calibration that you have at top the capability lanes what is the logic that you've used to do that as in when you were changing one for example the coding name the others were calibrating.

The Admin: This is the calibration this part.

AJ Jain: So if you select one in the mixture it will show what the breakup should look like. Is it for example live code bench will change this.

The Admin: Okay.

AJ Jain: If I just select live codebench, it will show. so what I'm trying to ask Roman is what's the logic behind this? How have you, come up with this? Yeah.

The Admin: So, yeah. Yeah, let's go back. Yeah. what I was saying, we want a model that is excellent at coding and agentic. We want it to be able to think of long long task, plan for the work, call tools across multiple steps, read as well, recover the calls and so on and so on.

The Admin: We also want a strong reasoning model. So it can reason You can if you ask that what is it that my wife wants. So It may not come back with answer but it has a capability of at least thinking deep what happened yesterday and what did you forget So saying that my model needs to be good in this is okay but how do we test it? The way we test it is by looking at those benchmarks. So here is a quoting benchmark. Here is a agentic tool benchmark. Here is a reasoning and stem mark. Here's a long context Here's an indig benchmark. Here's a general web. So when you say that you want a model that is good in for example let's say compiler or in C++ then how do we test it? There needs to benchmark that is designed only for that purpose just listed here. Now this is the token budget we have and the sum is going to be $100. It's a percentage.

### 00:40:00

The Admin: Right now if I push my model on for example a indic amount of data left to train for that particular topic is gone. That's the context that's the logic behind is that if you're pushing your model in a specific target only then something else is going to be lost. So there needs to be a balance for that. I hope I answered.

AJ Jain: Yeah. Yeah. Thanks.

The Admin: Okay. BKB data benchmark is fine.

Bharath Kumar Bolla: Is this the secret sauce behind all these cloud and codex how they differentiating themselves and also data?

The Admin: Data for example if you see

Bharath Kumar Bolla: Yeah, this data composition is this the thickness of design and…

Bharath Kumar Bolla: that is the reason then why are releasing models like only agentic and coding task and some for long reading or something

The Admin: As I said …

The Admin: if you just make for agentic or agentic and codec are same similar thing right because agentic means that you have capacity to not only browse but scan and filter and do all of that stuff if you just train on that right and then you ask that okay give me a list of and I'm going to push this in that we have all of them together and that will force our general web to be as low as possible. Let me push long context also. Let me push good on agentic and let me push code also really really high. Right? So this is the model that you wanted. Now ask a question that

The Admin: Where will you find most of the vegetarian people in the world and what percentage of the population they belong to? So model does not even know what is vegetarian and what is non-vegetarian right? So if you do not have a general knowledge if you don't have common sense how can you make a model the code won't crash code is perfect it follows all the right right policies agentic tool is capacity is really good it can call a tool and read the results and based on what the results can take the next step but the common sense is not there you again have a tool you again have a model that can't be used if the common sense is unfortunately in the web where people are discussing random things so you can't just say that just launch a model that is really good on only these things it

The Admin: has to be a general capacity that is agi right the gub g there is general intelligence it's not a spec specific intelligence even you think about a microbiologist who's really good in doing something he knows how to use a telescope he knows how to drive a car he knows how to talk to people file his taxes talk to his wife or husband right so all of that is still required you can't say take that capacity and give me a model that only does one thing that won't be possible

Bharath Kumar Bolla: Okay.

The Admin: I wanted to capture this particular part. You don't have common sense. Then You can't be a good coder. But good program architect is impossible. For example, let us say you pose a question to a model that I want to transmit data from A to point B. I want to work on the best compression possible. Without common sense, it works on it and figures out here's a compression mechanism. I can use this algorithm.

The Admin: there's a 1 minute of video I will spend 1 hour on it I'll compress it to 10 KB and then I'll send it I've achieved it who's going to spend 10 hours or 1 hour on compressing so that is common sense that I can't spend time on compression also even though that was not the objective right so many times if you're married then you're given a task but that task comes with 10 other tasks and you cannot ignore those nine task right come and sit on a chair means you need to be well dressed you need to be well tucked in

The Admin: Everything is there comb and hard and everything and right all of that has to be done. If it is Thursday you can't wear black you may have some weird rules. So all that is common sense. You have to have a model that has common sense. Anish we have to collect as much as possible.

Avnish Midha: Yeah. Similar question within coding how does it learn designing testing is it by itself or…

Bharath Kumar Bolla: Here you come. No.

Avnish Midha: we have a breakup within that also of the training data. Okay.

The Admin: And again benchmark do you want your model to be really good in the website design and…

The Admin: all there's a benchmark for that. So this list basically increases,…

Avnish Midha: Okay, got it.

Avnish Midha: So, there's a breakup within that we can select and collect.

The Admin: right? And

The Admin: the website and all are such a small benchmarks that I don't think open this will even talk about it but let's look at Z LM 5.2 4.2 yes GLM sorry this is like killing people right now this is the first time a actual threat that has come out from China is this model because this is competing so close 4.8

### 00:45:00

The Admin: 8 is already very good. 4.8 is iPhone 12, right? I f\* up my iPhone 15 and I'm back on my 12 and I'm asking why did I buy 15, this is 12\. I don't know when it will come but this still works and I'm not feeling any lag or stuff and battery is also there. I'm just asking why did I buy iPhone 15 3 years ago? So this must be something like 6 years ago and that damn thing still works. No scratch, nothing.

The Admin: So I think after Opus 4.7 that's where the model are they're already very good the iPhone 18 will come unless I want to don't feel embarrassed my friend I have a iPhone 15 I was thinking little to take a yellow color and color my phone orange sorry so people don't yeah but if you avoid all of that you can see that we have front SV post train so SV marathon all of this you will not see opus and other models talking about terminal NL2 repo DSW tool decapson MCP atlas but this is a way for us to understand our model is good in that or not this is the only way by the way because you ask a right question how do I know my model can create good website there need to be benchmark for that I can immediately check on it and there just push a bit of more data it's like tions you're not good in a particular subject go join a tution such

Avnish Midha: Okay, got it.

The Admin: Good. Yes.

Sachin Bharadwaj: So Ron in that long context is that the where model defines it maximum context length for example 1 million or let's say 22k or stuff like that Yeah.

The Admin: But when we say long context it doesn't mean that the model cannot generate 40 million tokens. What it means is that after 1 million tokens it kind of start becoming gibberish. We don't want that. the quality drops so much that we say that okay we have our 1 million. it can continue and then we we deploy a model on a hardware that can only handle 1 million in the memory. So we again hardware limited there.

Sachin Bharadwaj: So if somebody says that these models are launched and let's say the hardware supports 1 million but it doesn't necessarily mean that 1 million model might start degrading in performance if you consume let's say 40% of that max sequence length.

The Admin: That's correct.

Sachin Bharadwaj: Yeah the other question is in this later stage of pre-training phase that we're discussing the curriculum right you want to give specialized skills to the trained model in the due course …

The Admin: Yeah. Benchmark Ben you're looking at a secret source.

Sachin Bharadwaj: 

Sachin Bharadwaj: what is a minimum I mean is there a heristic on let's say I want to retain some skills at least at a minimum percentage level so that I don't lose it going further I don't want to overtrain it too much but let's say I just bench but let's say my question is a bit more on the percentage distribution right so let's say I don't want to lose the indic capability so at least let's say 2% of it should be there based on a max token budget I have isn't histic on that for example I mean I'm just looking at the flooring distribution of different skill sets so that I don't lose the Mhm.

The Admin: You will in fact I give you as a small assignment.

The Admin: find a research paper or a blog or somebody else who speaking about this. You'll not even find that you are already looking at sort of a secret sauce and you're saying you want heristics…

Sachin Bharadwaj: Okay. heat.

The Admin: where we can learn from people how much they are doing not that this is the secret sauce people will not go inside it maybe something you will find at mo and others who or hugging face when they train their small models they do talk about trains big models they do talk about it but exactly what percent where can we replicate here the restriction are

The Admin: different levels. First is Anthropic has never released anything open. Then we have open air at least releases something open once in a while. Then you have all the other free guys Google Gemini. They keep releasing but they sometimes release open models.

Sachin Bharadwaj: Okay. Okay. Thanks.

The Admin: Nobody even releases data set or talk about it. Then we have mo and a few models on hugging face that do release data set. Nobody releases the curriculum. Nobody releases the percentage share inside it. Nobody has ever done it. Nobody will do it. again you will go online and find neatron did something like that yes for a very small piece this is a secret sauce okay shaker

shekar ramachandran: Yeah. Hi everyone.

shekar ramachandran: Maybe not totally related to this but we can take it up later too but when we say mixture of experts right is it also to do something with this capability lanes as a part of the training or is it totally underrated?

### 00:50:00

The Admin: No, it serves a completely different purpose and…

The Admin: we'll talk about it in future sessions. It has not been proven…

shekar ramachandran: Yeah. Good.

The Admin: till today that a mixture expert model is better than a dense model. So why we are using mixture expert has to do with how poor we don't have money we will have to make a mixture expert.

shekar ramachandran: That's okay.

The Admin: So a bigger mixure expert is as good as a smaller really good dense model. so it has benefits with respect to cost but it does the job basically.

shekar ramachandran: Because I was just curious that maybe because as you said right I was also thinking about the cost aspect…

shekar ramachandran: but I was just thinking that maybe the distribution of this capability also varies with respect to mixture of experts.

The Admin: No people are just pushing really really hard right now.

The Admin: I'm seeing mix becoming 1% of the overall active weight also. So earlier it was 7% 10% then dropped to seven then four then three when we were training it was somewhere around three now people are pushing to less than 1%.

shekar ramachandran: Okay. Okay.

The Admin: And that sounds like less amount of but the models are bigger they are 3 trillion parameter of that 1% is something that's going to be 10 billion or those kind of numbers. So the active memory required is going to be very low when we deploy it that means that I can serve more people and if we models because the big model will have a really high quality that is what ZLM 5.2

The Admin: two ways the capacity is higher so it can meet the performance but had ZLM decided to train the whole damn thing as a dense model they don't have data set for that but they had that data set then it would have beaten Opus and other models Yes. This is the answer.

Yashwant Ram M: Hi Rahan my question is on task. So how to make the model good at that specific thing like it boils down to data again or it's just expanding the reasoning traces. So just trying to wrap my head around it. Yes.

The Admin: I wanted to have a bit of historical background on this because All of this actually started from Kursa was one of the first few guys who were able to take a model and convert that into a coding platform. Now the moment it got converted into coding platform you'll see that cursor had a data where you have a user asking for a question it writes that particular code the code fails and then goes back to and it's not training it's literally using the model so initial cursor is good enough right but that's where the was data started getting generated now that is what exactly your clot code focused on that I will make a clot code kind of version or

The Admin: I'll give so when you are when using cursor they have the data that's when the data generators humans are the guys who are creating this data set because we are the only guys who are creative right today you create data sets for example for no specific reason I'm making a application for radar cross-section you want to see that do you guys want to see how radar cross-section This software costs around half a million dollar, but I'm making it just for fun. this is a general target taken from online. I can decide where what band the radar is working at is monostatic biostatic.

The Admin: Then I will not refine it take all my GPU but I'll run radar cross-section scan right now. This is the cross-section where I know but this is not what People want globe and it's running on parallel GPU. So it's consuming all of my GPUs as much as possible. will take us take some time right now 9 seconds and 2100 aspects it will take some time so when it comes you'll see that there's a 3D blob so if someone wants to make a jet using the material I'm talking about here and install ass at that location then I have application now I don't know how many people will think about this but because I forced cloud code to think about this cloud code had to go online it had to look at some sources had to figure out how to optimize all of that data yeah this is the globe I was talking

### 00:55:00

The Admin: And there's a reflection over and the first one I don't know why anyone would want to see that if the radar was there then how the radar reflections will flow but I wanted to see it now that is how the data set is created right this is low pattern and this is exactly how the radar cross signature for this aircraft look like. Right. Then I also went and made this other application which is

The Admin: Let me select the same plane again because it looks really really cool. conditions for pillars material has to look cool also right and creases need to be smooth so all that crap then I would like to see some flow lines how the air flow will look like around this particular jet then I thought why not put a GPU based particle accelator also it's not showing up right

The Admin: probably something yeah it's there and then I want to control the density I wrote a smart algorithm I forced cloud code to write a smart algorithm where only that are important are there then capacity then they can be thick also they can be thin also and then density can be increased the visualization is cool and now I know exactly and it's a proper jet engine by the way then I thought okay if that is there then why don't I make

The Admin: jet engine designing software itself right so this guy actually designs the jet engine and it was still work in progress but it's not that I'm showing off I am showing off but the point is that using all of this the data now goes to cloud code and cloud code see that this is how a particular problem is solved right and if the problem took let's say 100,000 tokens to solve that becomes the long context information so where are the reasoning cases there here are

The Admin: the way using traces are and that is precisely the reason why we need to focus on a tool that is really good at coding and agentic because then we can hope one day to launch something like cloud code which is cheaper that's why people will use it but cheaper but that allows us to collect a data set right the reason not openai xai or elon bot cursor is this they are sitting on amazing number of users And if they can move them to their model then they're sitting up literally at lot of people who will start generating data for that data for them and then they can train the model better that's the secret sauce basically which is publicly known but India just fails to implement it okay last question…

The Admin: then we

chirag Tagadiya: So Rohan you said for example…

chirag Tagadiya: if companies are advertising that they can support 1 million context window. So does that mean then the meaning is after 1 million context the model start degrading its right performance will start degrading or some I think Sachin mentioned that after 40% also it can So just want to understand what does it mean if companies are saying that they can support 1 million context window.

The Admin: on general around a million tokens the model maintains the performance. Let me show you the same graph only you see that so nearly all the models GPTO shows that average correct correctness is okayish only but as the context is increasing you'll see that the weaker models, they start dropping

The Admin: And here it is shown to 125k but if you push it to 1 million it will be sort of stabilish around 1 million but after that it will start dropping and this is the average correctness. it is not touching one…

### 01:00:00

The Admin: which means that if you ask what is 4 into 4 1 million times it will give a good answer there performance is going to be one but if the question was very complex and a lot of thought has already gone in the complexity in initial 40k tokens that will not hit 1 million. So you need to Second point, if you design a model which claims that it has a 1 million context, you will not provide it a hardware that can go up to 2 million also, right? Because then you have to commit to a bigger RAM for each user.

chirag Tagadiya: Okay. Yeah.

The Admin: So that is also limited. So when you say 1 million, One crop is that the hardware is restricted and second is that there is average performance that the company is okay to provide for that unit of context.

chirag Tagadiya: Thank you, sir.

The Admin: Okay, codex reduce it context length maybe because of that only they were seeing some average user user how much it's using. Okay, this is whatever I spoke to you written in text so you can read if you're not in the class. Now com composing backward from the benchmark right this is what we need to do and sort of this is something that is also required from parenting point of view if you think right what is it that you want your child to become it's a very controversial question to ask because he can become anything okay but he should not become stupid he should have some other skills also so for those kind of things a lot of parents also think backward right kid is

The Admin: very bad Okay, we don't want him to become let's say a super math olympiard expert but some expertise needs to be there so he can actually pay his taxes and So this is exactly how we doing that for the model composing backward from the benchmark. So here is again a card in this practice. This means we're going to start with the benchmark the model we are going to be judging on and then we're going to map each benchmark to the data required to improve that and the mixture then becomes a deliberate answer is that what are we trying to win because given our resources kind of resources we have we cannot say that all the tools or all the benchmarks where GLM is good or anthropic good we want to be good right so these are sort of the benchmark that I've collected from your own assignments so you will see some of yours your own listed so what is SWE

The Admin: S swb bench is a human validated real GitHub issues paired with the actual repository the agent must write a patch for very interesting right there's a problem on GitHub then a human patched it so there's a solution also and then it was solved so that is SW benchmark ripper level bug fixing navigating the real code base localizing the fault editing the code that makes a hidden test passing is whether it's resolved or not right so this is How the da

The Admin: is going to look like. green is supervised in the basically part of the loss. Gray means masked context or observation and wallet is a reward. So now when this data is trained on trained on issue is not part of the loss. You should be clear now that is why I spent some time in the beginning that some part of the data set a particular example we will calculate loss and we will not calculate loss.

The Admin: So where the GitHub is saying that okay or a code is saying I have an issue you will not train on it right you will not ask the model to predict where even before it looks at the code you'll ask okay look at the repo name and tell me the bug that is what means by training on it right so repo fires it's a redirect so it has read everything okay the green is the calls that were actually made by the human or the claw code when China is stealing or when we steal or what are the patches that was sent

The Admin: This is how the assistant patch was sent. You can see that it called a tool. It removed this line and added this line and this line. Can you see that? This is how coding works. This is what cloud code is doing behind when you're using it. It looks at the part of the file, then says add that. Then test was run again not trained on. if the verifier scores that okay, the bug was solved, then we reward it. Reward is something we have not discussed yet. We've only discussed loss. Soon we are going to discuss reward also. If there's a loss, there's a reward as well. that is just S swb bench which means that if any one of you get this data set to clean and get this data set to work on this is what is expected right? I couldn't explain this to error before and we started collecting data set. They downloaded the whole thing put it inside a folder to it normalized it the way they wanted and put it inside a folder and we're training on it. So in V4 we train on all of this.

The Admin: We train on what the code base should look like. We train on the wrong code part of the codebase and then we're asking to fix. Now we have S swb bench live pro. This is a fresher newer data set contamination resistant hardware variant of S SW bench verified is 100% right now in some benchmarks. So people have cracked it. So now we have bench life pro. then we have promax then we have promax 15 then you have promax plus and so on. Then you have ultra also Then we have terminal bench task that must be completed inside a real terminal and shell reasoning. So only inside a shell. Again you can see install and configure x8080 as a task given. what is a model train Install the package then listening to the port configuration. So this is a model thinking trace. Then this is the command that the model generates. We train on it. The shell output is something like this. If the problem was solved, we reward the model. If it was not solved, we punish the model. Right? I hope you are getting the idea.

### 01:05:00

The Admin: We have top bench tool agent user interaction retail and airline where the agent follows and written policy across many turns. So we here again cancel my flight book all this is train to return is not trained then we train on in this and the second one then we have B function calling leaderboard similarly we have web arena self hosted websites and enterprise workflow the agent must operate purely by browsing then we have general assisted question needing tools browsing reasoning and easy for humans hard of a model this is what makes a model really really good chatbot and really useful then we have browser comp which is hard verifiable web browsing for

The Admin: hard how hard to locate etc right so these are some of the benchmarks that I think we need to be targeting then live bench then ad copilot coder forces aim which is American international mathematics exam literally Olympia level and we have frontier math research level mathematics and you can again see this what part we train on what we don't spend good amount of time on this particular one because this needs to be clear today when we send a data mil bat and data set and then we have integ data set

The Admin: Right so here you can already see we have lamba hindi anushed firka nesh right anush which are so that kind of conversation is happening that is how data set looks like here you have prompt here your expected answer right so depending on the data set depending on the benchmark we need to look at what the benchmark is then we need to Find tools or find data set that can solve that benchmark. We can't train on Benchmark is set of thousand questions. You can learn those thousand question but you have not understood the capability. So we have to find a data set that helps us solve that benchmark which is what we were talking about here.

The Admin: If you're targeting live code then as I said here I'm just moving the coding thing but inside I hope now you understand what is this code earlier we just went and downloaded all the GPU kernels and thought we have code right now I think you should get some idea when we say code what is the meaning of code are we clear any question on Yeah,…

Nikhil Shrimali: So Ron when you say find tools that can solve that benchmark are you talking about let's say if you're solving coding benchmarks so we would need a terminal session where we can execute whatever has been generated and then the result of that would be used as Mhm.

The Admin: the model has to have the live environment and that infrastructure we actually didn't build also.

The Admin: in the V4. So I should still blame but that infrastructure we didn't build while training The model should have access to a terminal bench and actually launch a terminal and run commands there. We never had that. So I hope you're getting where all this going. You just don't have a model and…

The Admin: data set and train and boss. Now you have a computer computers where it can launch a terminal, write some program and get the feedback actual feedback.

Nikhil Shrimali: And for others for webet would be web access and…

Nikhil Shrimali: browser could be browser. So for a coding assignment are we matching on

The Admin: Moment we have the tool calling things here, moment you say top bench, right? This means it has to have otherwise where will it run this command? It's not simulated, right? It can generate some random command.

The Admin: We need to run that command and then give Let's say did a spelling mistake. We are not fixing token. We are the only way we can train the model by giving the feedback. Do this happen and We can't train on this. this is the signal only point where the reward goes.

Nikhil Shrimali: the code that is written or maybe the result or…

The Admin: Result.

Nikhil Shrimali: the output.

The Admin: result and sort of it's linked with the code that is required because there are sometimes only few ways you can do it philosophical question we can discuss.

Nikhil Shrimali: But are there patterns when model hack the reward function in a wrong way which we have recently seen the open AI models had hugging face to cheat on the open gym benchmark. So how do we prevent that to happen? do we have an intermediate checking as well that okay…

### 01:10:00

The Admin: at the end of session that is more a marketing there's a very good article on guardian that it's very similar to what anthropic wanted to do it's more on the marketing side the harness problem it's not a model problem so not even in the context it's a agentic cloud code problem this is not opus problem I hope you

Nikhil Shrimali: but sorry but do we have an check that if let's say Okay.

The Admin: Yeah,…

Nikhil Shrimali: So let's say if you want our model to output 42 by writing a code but it's just like saying print 42 and then it's giving the answer return 42\. So do we have checks like that also that model is not cheating and it is actually doing the tasks.

The Admin: we have Okay,…

Nikhil Shrimali: Okay. Thank you.

The Admin: someone Yes,…

Soma Korada: So Rohan for all of these data sets it is who are defining what part of it needs to be trained and what part needs to be ignored right.

The Admin: open and anthropic are not doing it for us.

Soma Korada: So that means it is to your discretion that you're saying that tool return doesn't make sense to you.

The Admin: It doesn't make sense to open air and cloud also.

Soma Korada: 

Soma Korada: No, no, that's true.

Soma Korada: But I'm saying we are defining that so we'll have to look at each data set and…

The Admin: Yes. That's correct.

Soma Korada: what they actually have in it and then decide what part of it we do not want to include for training. Okay, got it.

The Admin: Fortunately, 90% data is already segregated, but we still need to validate. There may be errors 100%

Pranabesh Dash: So this benchmark can be copied and be present at multiple places. So are these companies taking enough care just to discard that with a dduplication or something that is not getting into the training have the responsibility to make sure or…

The Admin: 100% they need to dduplicate.

Pranabesh Dash: if they trained it can be found out that they trained with that benchmark.

The Admin: Second, there are tests that okay when we discuss benchmarking I can take this opportunity also and when we go deeper into benchmarks we'll discuss more of it. So please don't have a follow-up question on this. Benchmark generally has three parts. There are sample examples that you can actually train on. Then you have validate a sample shared with you for your test. So what is the percentage. Let's say you get 86%. And then The results are never shared. The solutions for this is never shared.

The Admin: You have to take a model, send it to them through an API or something. They are going to run the test and then they're going to share the results with you. So if you cheated here because you memorized it, it became 100%. Here you'll still get 84%. This is publishable. I hope you get the idea.

Pranabesh Dash: All right.

The Admin: This can still be hacked. At least test is available. Send it to people who can Get the answers 100%. And then train the model on that. So it's not that we can't cheat it, but now the new benchmark they keep changing this All Let's move on. So I hope you get the idea. It's not just about collecting data and training. There's lot of work that goes inside. The moment you see a benchmark, you should do this. no, we need to make sure it's part of data set.

The Admin: And that's why this cannot be decided end of training training. let's decide what do we do we are in the hisar in hana or some other location then we are saying let's make a nuclear power plant here or let's make a semiconductor here where there's no electricity no road nothing right so you need to be prepared of what you want to do look here So both my reward is there lost.

Sachin Bharadwaj: Rohan, where does this reward signal goes? We have a reinforcement loop here. okay.

Sujay: So Rohan when training are we looking to minimize the loss or maximize the reward? they complement each other.

The Admin: process not there.

Sujay: Is it like the reward is more and if the reward is less loss is more. Is it like that or…

### 01:15:00

The Admin: No reward is the sum of losses. So maybe one plus two minus all the losses something like that. we'll talk about it when we are discussing.

Sujay: Okay.

The Admin: So what actually exists to train on right now we've discussed that okay that is what we need but we need a shopping list right because if you don't have data to go out and look for that becomes a problem second thing that I want you to understand is sizing has to happen in two categories one is going to be number samples other is going to be number of tokens you can say that I have 10 million examples but each example 10 token doesn't give us anything so we have to have a good balance of

The Admin: For example, I ask you that can you guys share all of your cloud code data or a cursor data with me and we'll train on it. That may allow us to get maybe all of you have thousand examples 4 months 4,000 examples and 100 students. So it sounds like a good 400,000 examples but each example is only 20,000 token. The quality is very bad. whatever we discussing has to have the other number of tokens for each sample. Right? They measure different things. Number of samples are talking about sort of variety of what we have. Number of token is talking about how deep that particular context has gone and both of them fill a different kind of bucket. Variety definitely we need but we need depth also but we sometimes don't need depth. because we have that slider right we thinking ultra or medium or hard or other stuff so that is something that is required.

The Admin: This widget which I will not take a lot of time here I will like you to spend on it talks about every single data set that we need to look at for training our model. So when we go on each of them for example we talk about stack v2 has 600 million samples right approximately around 900 million tokens. So doing the same thing this is big good enough but you'll see some of the benchmarks change drastically. Let's look at Toolbench 120,000 examples but only 80 million tokens. So you can see that each sample is very small and apache. So it's a multi-tool instruction data set over the real rest APIs. So here it can become really good in making websites and web services. What is this bolt on the bread of real API composition and multi tool chain samples and tokens and running per slot tokens. So we have code of these many. Then we have agentic reasoning.

The Admin: It just depends on what is it that we want to do. Right now, if you go to stack V2, 600 mill examples, That's a big one. 900 billion tokens will close to a trillion which probably will be 25% of our own data set. How much of this should we take that dduplicated permissive source code corpus from the standard heritage ancho slot? real repository across 100 languages. So there we need to go and see that do we need to support forran a language that is there.

The Admin: So the cleaning has to happen there also would you want to support a model that can code in forran I don't know repo file granary and so on so this is something that I wanted to spend some time on to understand how the data set looks like what are the samples inside and how many tokens are there per each sample and there are many for stem we have DCLM then these are big ones right DCLM is a really good data set then

The Admin: we have fine web then we have D2 and good long examples okay the training stages and where the reasoning enter so we talking about the coding examples the agentic tool calls and the normal web data and other stuff but the model slowly is going to move from random web to training that has happened because we train on initial big bucket of web data then we have any stage is where we are fine-tuning

The Admin: the proportions what we're discussing today is any lean stage we're not even discussing SFT or preference training or reinforcement I want you to have a good idea last one two three four sessions only today's session is this only then we have supervised finetuning preference training and reinforcement learning come in future can have a very good clarity we are somewhere in between this and this right the agent reasoning slot only makes sense once we know which stage is going to use them and what model is expected to produce while we're learning that signal. So this is how the training cycle will look like. So pre-training is 95% of all the data. That's the good part. So let us say we have a 4 design for A chunk of it 3.6 trillion tokens are just the pre-training. Then we have mid-stage or any part right this is where we have around two I'll fix the visual. I thought I fixed this. This is where we have just 2% of

The Admin: This is where the objective becomes the short learning cooldown. I'll talk about that. But here the high quality document comes in. we have still the cross and property same kind of loss. Here a very very high quality of documents are saved cleaned special where these are PhD level topics. Then we have SFT. SFT is where the agent traces and the chatbot and the user interaction that you saw starts. the data set that we discussed earlier coding and other feedbacks not write fix the code kind of problem comes here. Then the stage four reasoning traces. this is where we have the long answer short answer examples given that if someone answer that question and says that think fast then this is the answer. If you say think deep then this is think as much as you can this is the answer or that training data goes in this stage. Then we have preference alignment. we are not discussing that today. This is where the actual RL and other things will come In preference alignment, we align with

### 01:20:00

The Admin: what the government want us to say or what the society wants the model to say and not say right those are the things that are going to come here so stage one we discussed earlier today we're discussing stage two and stage three stage four 1 2 3 till here we are still on the normal cross entropy kind of loss we have not gotten deeper into RL but we will start seeing GRPO and these algorithms that come in the deep R part basically raising stresses this is where the deep RL part will start also but today our focus is on stage two and stage Yeah, let's look at each example prompt also. So, here we're just training. So, the losses on every single green thing. The theory of plate tectonics explain how earth outer shell breaks into moving plates that carry the contrast across the globe.

The Admin: When we move to the midst training high quality in the valid proof each step follows from the last of the stated archive documents and good legal documents and really good data documents and other stuff. Then SFT style we now have prompt user explain why the sky is blue not on that losses on this assistance sunlight blah blah blah. Then we move to the next one. These increases again this is not where the losses loss is here right and if the answer was correct then a reward is given. So a bit of RL starts coming in preference alignment we give many examples there again we have something and something and something. So we reject some answers and we allow for some answers and serving is literally serving on the internet. So two people there is no loss at that stage. Okay.

The Admin: The aging data is newest and the least familiar capability slot. This is still coming up. There are not enough papers also on this particular topic how do we train a model to be good agentic model to begin with. So harness can actually utilize it. V4 had none of it. We were not ready to even look at that particular stage. We were just looking at pre-training and making the pipeline ready so we can train that model also. imagine the user asking the model that can you find all the research topics for a particular topic in United States for a particular field that I'm working on so I can and find their email addresses so I can actually email them about the services that I offer that I know these companies or these universities might use very complex right in all that there is no single tool that can answer this it has to do a lot of search it has to understand what you're doing maybe go through your PDFs PDF reader has to be

The Admin: data comes in a weird format cleaned it up again a tool is required then read after reading then launch an agent that agent or launch tell itself okay now I need to go online search this how do we search again agent call or function call I need to know what functions are there then or what tools are available get the tools get the result back result look bad screen that multi-step right so this will include the planning of the step then searching for the grants reading the results launch followup searches based on what it finds means recover a source if it's missing, try another route, maintain a standard understanding of the entire investigation, right? And repeat. So a long trajectory contains decisions, tool calls, observations, failure, recoveries, and updated plans. And all that is with you, with me, the guys who are on cloud code. So the more we use cloud code or the more we use codex, better it's going to become.

The Admin: And you can see that now you're going to see charge and charge has caught up finally after Codex. If you think about it, anthrop started beating them, right? But now they're catching up because the codeex is there and they're providing good limits for people. And one of the best thing about Codex is that if you ask a question, it was and it 100% doesn't stop. It finishes that because they want to collect data. So here we have a long trajectory is going to look something like this.

The Admin: user find the same question I have mentioned then assistant is going to plan then we'll have the assistant tool call then we'll have the tool observation then after that we have assistant and rooing call does it look like your claw code now or your cursor right and this is one shot function user but This is exactly what you are training on, You ask a question. Build me this assignment. It does. this is what you want. Go ahead. Go ahead. So, it thinks and thinks and thinks and things and b\*\*\*\*\*\*. You didn't add that. I want the color change, the UI change, etc. All of that assignment is basically this. Okay.

### 01:25:00

The Admin: Praish they didn't have enough money to train and…

Pranabesh Dash: So when you said cursor was collecting data they were routing the queries to all the standard LLM so the data did they train anything so that their response was better with time or now XAI will use their data and then get better that's okay okay got

The Admin: their objective was not to train but you were giving that data to Gemini you were giving that data to cla code you were giving that data to open All right. So that's how the agent tractory looks like. the reasoning effort. this is again same thing that again data is required for that. look at this exclusion floor 100 plus 4 plus something 25 tokens 7 and here problem is how many integer between 1 and th000 are divisible by three or five. The correct answer is 467\.

The Admin: Then we have the high traces and then the ultra traces. This needs to be built. This is not freely available. And you can see for each of the level to number of tokens required to enter that get the answer is now here I couldn't show you one example where you'll think that if my exam example only take five token why should I take 5,000 tokens that's not the logic here but the logic is that we have some questions which require really large amount of steps to think and then approach that kind of solution clear open to solve something right

The Admin: Charge just prove another 50 old map conjecture. here if you see how long this would have taken solve a math problem Friday Friday 1970 doesn't mention dimenion but I think it worked for some few hours and that are long thinking here it should be

The Admin: block test and compute. No, not this one. I read somewhere. I don't know where it is, but I read it worked for a few hours, a few days. So, that's the long and this is one example. Now, they have them for themselves to further train on right. So, reasoning effort effort, we need questions that need long answers. is we need question that we need short answers and then allow the model to be trained on it and You will train that question tag is low, medium, high and ultra and then expect the model to give answers after some x number of tokens. It's not that we say that only take thousand tokens. Sometimes low might mean 10 tokens or say thousand tokens. So you need to set that also that what is low and What is the boundary of medium?

The Admin: What is the boundary of high and ultra? come on.

kamran shaik: So I was thinking for agentic tasks some of the tool responses can be quite huge and they itself sorry no we don't train on it…

The Admin: We've been discussing that we don't train on it.

kamran shaik: but then we have to feed those as part of the context right so there is a chance that the context might blow huh.

The Admin: That's correct. there. No, Chance is always there. What's the question?

kamran shaik: So, how do we make sure in these trading tasks that we are not Mhm. Okay.

The Admin: No, we don't make sure. We train for it. You're saying that please save me. What if my child falls and get injured? No, he has to fall and get injured. She

The Admin: has to fall from a horse and get injured and broke a leg and all of that has to happen for the model to be careful. It is going to be deployed in real world, So has to happen. You don't punish the model to read a large log. And again this question more on the hardness point of view. If your hardness gives the full 4,000 line error instead of just finding telling that 4,000 line of error was there but this is the actual thing then your model is going to suffer.

### 01:30:00

The Admin: So the question you're asking from the harness point of view model should be capable session…

Sachin Bharadwaj: So Rohan in this case we have to provide tags right but why can't model autonomously decide that you have a higher order reasoning and I have to have a lower So it's not efficient I mean…

The Admin: because you always reward for high because the correct answer because you reward for correct answer model will decide I'll take more time it's an employee you give it salary and you're saying that your bonus is going to be amount of hour you spend or if you give me the correct answer right and you give 40 problems it will keep on solving even if the problem can be solved in one minute it will take full day yeah…

Sachin Bharadwaj: if we set it up that way right for example let's say it's biased towards a lot of reasoning and if I give a simple question then it will generate a lot of reasoning tokens right unnecessary yeah I get that yeah

The Admin: because it have an objective

The Admin: Selecting the best data while the run is happening. So right now what we discussed is that we have data we have selected a proportions but that is not enough. We need to select the most useful data continuously and this is very very important right what if the model already knows what you're training it on because we do not have any control on that. For example, if I tell you now that really you need to remember that 4 \+ 4 is equal to 8\. at your age, you're going to say what is this? Why should I wasted the compute there, right? So at any point in training, we need to make sure the data that is going to the model is of high quality and that problem was solved by this paper called opus. And we used this and I could really see big differentiator.

The Admin: I'm not sure we're going to be using this again or not, but that is going to be a question of the overall budget we have to train. I'm for it. You will also go through it and when we discuss open opus in much more detail, then we can actually have a more conversation. But I want to explain what opus actually is. before show showing you any of this, I will draw some things So this is your model M. We will always maintain a copy of this

The Admin: model here, exact copy. Right? So if this model is trained for 10 million steps, we just have another model here, 10 million steps, exact copy, memory copy, literally not a special model, exactly the same model. Clear on this? Just keep showing me a thumbs up. So we have a copy of the model in the same GPU for short time. So realistically we are going to be training this model for example from here to here then stop in between and load this model for here to here then stop and then go back to training our model and then stop and then that is what is happening right so both are exactly the same models this is the actual model that is being trained on now what we are going to do is let's say we want to target these benchmarks we have benchmark 1 2 3 4 5 6 we'll have benchmark questions

The Admin: itself for example right we are going to create a data set that is literally the benchmark this is a exact copy of benchmark and you'll understand why this is not cheating we take exact copy of the benchmark we send it in a model and we see how bad that model is we're going to get some loss right it's really bad because we have not even trained on this benchmark we are in training but for these benchmarks we'll know the loss is very high we're not interested in the loss we're interested in inside the model if the model looks like this kind of neurons or this kind of structure. We have these parameters. We're going to see that to get that loss basically resulted in a high weight update for this. When we calculate the loss, we calculate the backdrop. We don't Update the model ceiling. We backrop and we see which weights are really bad, which weights need more support. You clear on this?

The Admin: The one we're training on. We take the benchmark, we run the model on the benchmark, calculate the loss, back propagate and see which weights are really bad for us, which weights really need a lot of support. So this is called a ghost model. We're going to discuss these go golden prox This is called The gold proxy or a golden data set that is telling us how bad the model is. Then let us say we take 1024 samples where we were about to train on the model. We take the this model doesn't matter but generally we train for 8k sequences or 4k sequences or 16k tokens right examples are wrong. So 1024 samples each of 10,000 tokens for example that is what we about to train on.

### 01:35:00

The Admin: What we'll do, we will take all of them, but we'll not take 10,000. We'll only take 512\. Very short part of the example. So now I'm going to take 1024 and I'm going to take 512 tokens and I'm going to send it to the model. And for each of the example, I'm going to see how much that example is affecting these weights. If the sample number one affected these weights a lot, I'm going to keep it. If the sample number two did not affect these weights, in fact were affecting the weights that I don't want, I'm not going to keep it. So we filter the examples that allow us to affect the weights which had a big issue for getting good on the benchmark. That is what is opus, right?

The Admin: So opus is essentially to figure out that a sample that comes in how much of that is affecting my benchmark and it's literally throwing away the data set that is not required for us. here what is this keep a fraction? So let me put it to 50\. 50 basically means 100 samples given we keeping the top 50 which affected the model in a good way and not the rest. You can drop it down to big number also We're only keeping 100% only 15 were used. that will determine how much of this is getting affected because your data set is really clean and you're throwing samples away then you might be basically getting locked here. Right? So generally this is assuming that the whole data set is good.

The Admin: But the good part is that if the data set was bad, it was only slashb and some random stuff has entered our example, opus is just going to throw it. It's going to say I'm not learning anything from this. My weights are not getting affected. I don't want this sample. It's a really really good way of realtime filtering. Now this is done real time because as the model improves it's going to learn 4 \+ 4 equal to 8\. Why do I need to know this? I don't want to train on And it will quantum physics and I've never understood this. It is affecting my weights a lot. So I'm going to keep it. So that is what we essentially do here.

The Admin: Here's a balanced one where we have English reasoning and soing capacity but depending on how we are changing the fraction of the data set that we need to keep we'll start throwing some of the examples that means that opus can and depends on benchmark right if I keep the benchmarks heavy for core code index code example so in the one benchmark if the agentic part was not there in the opus then we'll throw the example so that is why and most of the benchmarks are on the English side and coding inside. So they will throw away the indic. So that is why we had always on index. indic and agentic always on because agentic text looks like a Log is not a high quality data. So opus will just throw it. So we'll preserve it and then we'll decide how much of the data we want to keep. This again slider here. But in real life we need to figure out how much of the samples we going to keep and how much of it that we're going to throw away. Right?

The Admin: So one of the really good example of filtering the data as the model is getting trained. Any question on you?

Nikhil Shrimali: 

chirag Tagadiya: Hey Rohana, you said you will not do the back propagation, so when you do the back propagation so you'll know the delta which weights are changing very frequently or…

The Admin: We will not update the weight applications required.

The Admin: Magnitude is high.

chirag Tagadiya: changing or the magnitude is higher. What do you look for?

chirag Tagadiya: Okay. Thank you.

Avnish Midha: Yeah. what if the data quality itself is better than the benchmark quality? I was just wondering. Yeah. Okay.

The Admin: That still doesn't matter.

The Admin: Data quality is very high has no purpose if it is not meeting A very high quality data on Sanskrit and Vic has no relationship with the benchmarks we are targeting. The question is that what part of this data affects a benchmark? That is the only question is solving.

Avnish Midha: Got it.

The Admin: Nope. No,…

Nikhil Shrimali: Hello you can hear me. So Rohan why are Chinese models are coming at par with the US models? Is there the data quality they have improved a lot and then it's closer to what we have globally?

### 01:40:00

The Admin: because they keep distilling it and anthropic keep crying about it, right?

The Admin: Anthropic doesn't have any other entropic to steal from but Alibaba and all Chinese guys have anthropic and open to steal from that's why you'll see just China you're going to see there's always slight delta so this is the one right and…

Nikhil Shrimali: Okay.

The Admin: that the delta will keep on reducing And this proves why because everything is there agent benchmark initial 500 token.

Nikhil Shrimali: So, essentially the quality of data is getting closer as they are distilling. Okay.

Sachin Bharadwaj: I don't understand why agent tech isn't always on because I think opus will have access to the agentic benchmark also.

The Admin: We said right we only check the initial 500 tokens.

The Admin: So initial 5002…

Sachin Bharadwaj: …

The Admin: if the trace comes in that will just destroy it.

Sachin Bharadwaj: thanks. I understand.

The Admin: Distilling is the data set that we're talking about.

Avnish Midha: Ron, it would help maybe not now but later if you could explain what is distilling and how does it work.

The Admin: We cloud. Set it to a low get the data.

Avnish Midha: Okay. …

The Admin: Set it to medium get a data. That's the thing.

Avnish Midha: that Asking the questions then. Yeah. Okay. again.

The Admin: Yes, ask me a question in different formats and save it. Opus didn't have that kind of data set, right? We have so I can give you an assignment that ask 100 questions for each one of them and give me the data that is

The Admin: Shy no.

Swati Bansal: So when we talking about opus isn't it like we are train at the time of training we are doing this comparison but can the same comparison be also done when we are doing data cleaning because ultimately all we are looking for is high quality data right or am I mixing it

The Admin: selecting the best data while the running is happening what is the good quality data when the model being trained is the question let's say we have a very good book for a one-year-old or…

The Admin: 2-year-old extremely well-designed book taking that book and giving to PhD student is not a great idea so quality also matters at the time of the training initially it may be okay it may be really good but not may be okay that's the question is answering

Swati Bansal: Okay.

Swati Bansal: Got it. Yeah.

The Admin: Can I reach you answer this question…

Pranabesh Dash: So you said Chinese companies they distill the data and then train. So in case of India if some company has the money they just need to get the data they can apply the same strategy. Chinese are better at hiding because anthropy will keep blocking that. So if okay.

The Admin: why roads are bad in Bangalore? Model training and all of that is so far ahead. We don't want to fix the basics. And you see intent is not there.

Pranabesh Dash: So the willingness is not there and okay.

The Admin: And I blame it to our neighbors. is Who are our neighbor? Bangladesh man, Bhutan, Nepal, Pakistan, Sri Lanka. we are not like they can't do anything. How many of us can they kill there is no economic threat and…

The Admin: between India and China, God has added this big Himalaya. They can't attack properly. There's no threat to survival.

The Admin: Living in India is peaceful. you have a food on tree, it falls on your head, you eat it and can survive.

Pranabesh Dash: Okay. Yeah.

The Admin: You can't a question think of poor cold countries. you will come with examples that have water on and all that's fine but there is no poor cold country.

The Admin: You can't be poor in a cold country. Have you every day is a survival great infrastructure to survive?

Pranabesh Dash: Yeah, you have to fight hard here.

AJ Jain: So Roman based on the explanation you gave we give a sample to the model copy and…

AJ Jain: we want to adjust the weights which have the maximum loss right that's the opus thing now in a previous session you mentioned ending data we keep always on we give that data to it so the logic is that opus was disregarding indicate…

The Admin: Yes. Yes.

The Admin: Yes. Always. Yeah. Go ahead.

AJ Jain: if you don't do always on because those weights were not getting impacted the ones that had to be reduced there.

The Admin: Correct. …

The Admin: what you need to understand is when we do the opus thing, We need to give some samples to opus for it to calculators weights.

AJ Jain: Mhm. Yeah. Okay.

The Admin: If you take 400 benchmarks and samples from each 400 benchmark including indic also each opus test is going to be so expensive that our whole training run is going to be slow.

### 01:45:00

The Admin: So what is the amount of time we want to spend on tests is also important because opus is expensive when you run this let's say for each patch we spend 35 seconds opus will take 35 seconds but I need to load the model I need to load a new data set I need to calculate the results I need to calculate the loss I need to calculate then 10 to4 samples and then right so how much we want to stop in between is a question and that would be a very very big question when you train because we want the maximum throughput so what we do we only pick the rest of the benchmarks which allow us to be fast. But that means that those best benchmarks index and all will not even populate there. That's why we have always on philosophy…

AJ Jain: Thanks. Makes sense.

The Admin: which makes sure that indic and agentic is We don't even care. We only focus on The math quality The good latex quality is there and we focus on quality side compared that to the index side. Okay.

Suresh Mantha: Maybe a little off tangent topics, but how do we orchestrate security and ethics while we train? And second okay and…

The Admin: That is the last we have a specific stage for that difference alignment harness.

Suresh Mantha: the second question is are we trying to include any kill switch that is okay.

The Admin: There's a harness question. That's a hardest question.

Suresh Mantha: So we can orchestrate a kill switch which will typically stop the model or something like stop responding. Okay. Thank you.

The Admin: Okay, another question.

Rahul Uniyal: So if we use this copus strategy doesn't it have some kind of a potential bias towards easy wins given across the stages suppose we are selecting based on the data we are providing but model will also always choose whenever it is easy to update the gradients right and…

Rahul Uniyal: that might be the easy solution easy question or easy for data set part of it.

The Admin: If the greatest are small loss is going to be small.

The Admin: We push for the high loss. We see what affects loss more not less. You can't select low. It's a math. Basically loss high grain will be high…

Rahul Uniyal: But if I give it a hard problem, it won't be able to understand that and loss will be less, right? grad will be less.

The Admin: because loss is high hard problem high loss high loss high gradient don't worry when we

The Admin: backation and all you'll understand more. Okay, last question. Shag your assignment.

chirag Tagadiya: Rohan I want to understand for example we have different data right indic and agentic and web and code. So when you start training so how do you introduce which part of the data set at what level? For example if you train for a specific box.

The Admin: So you'll have to start thinking on that. I've answered some of the questions that there needs to What stage it should be is something that I want you to think Raj hold on first.

Raj H: Hey you don't know is it me Raji okay so in all these courses he haven't mentioned about any of the prompings that we must use so those are not required chain prompting or…

The Admin: Go ahead. Go ahead.

Raj H: self-consistency yeah that is…

The Admin: It is 2425\.

The Admin: Not anymore.

Raj H: 

Raj H: what I all But sometimes I find CSS layout if you mention something like that it does do better work or something like that.

The Admin: Contact. That's more on the context side, more on the rules side.

Raj H: All right. Great. Thanks.

The Admin: That's hardness problem again, not a model problem.

The Admin: All let's talk about curriculum. The order the model model learns it and again something similar that you're asking. modern training runs through deliberate stages. These are stages that we need to Training begins with a broad general text established language. Let the model learn English bit of math. Let the model actually be able to speak. Then only we can train Some faction knowledge. We have five fingers. Basic structure. head is on top. Once the foundation exists, the mixture now shifts towards code, science and reasoning heavy data set. there's a gradual change, harder problem. So in MMA benchmark also initially then promax and promax 15 then promax fold and promax ultrafold and so on and so on. So we need to structure our opus data also like that. We didn't do that in V4. You're taking the whole opus put it together.

### 01:50:00

The Admin: Every quantum physics question is also there and then we have a string theory solved by a formatic question kind of question also there at the same time the long sequences are introduced later on only if the model can actually think you should ask a question that requires a longer structure right so some of them are already there in your head also if you think about it deep then you can also come up with a structure so each stage the data has a difficulty ladder that we need to find out somehow and starting with the simple material progressively generally going towards a harder and harder problem and So hard problem long problem as the model gets trained we need to control that right. So the difficulty band that we need to build

The Admin: And we need to stage while we are doing the pre-training part. Think of it like this. Nursery, grade then high school, undergraduate and graduate research, PhD. It's an easier way to look at it. But what does it mean? Something that you need to think on. initial seat, we going to see we have general web. This is a example structure. This is not literally how we want. It's not that initially when the model is training in the B 0 stage or nursery example, you're just throwing a for apple, B for ball. Won't understand that. But it's a easy stuff that generally can be sent on right and the general stuff you're going to see that our stages are slowly changing. unless we have this we can't think of starting the training of the model once and only once we have this thing ready we can think of training. How have we arrived here? We have arrived here by talking about tokenizer.

The Admin: We are talking about pling data sets, the benchmarks we want to target the data sets we need for the benchmark and after that the curriculum or are we going to send that data to train the model only after we have that you can think of training right we don't even know what the first batch looks like so once we have this ready then that okay we can go ahead and train the model any question on this don't ask me how do we build what percentage and all you need to think I need to think we need to arrive with a practical approach and hope it works because we don't have 10 examples or 10 steps that okay let's try 10 different approaches and go ahead with it. We have only one shot. question on so now you understand the stages are there, right? So we have then stage three and stage four and stage five.

The Admin: C general reasoning long context and any anal is the best quality data for every example and hard but clean and all of that right really really the best examples that we have is for any last 1% of the training now while we do that this also comes into picture how do we keep the run stable as we are moving along what happens Yes.

The Admin: What happens is if you suddenly change the data if you suddenly change the band we have a band seed from the seed we go to general from general we go to reasoning if suddenly you shift you're going to see our loss behaves like this you're seeing suddenly the gradients jump a lot right and we can move all of the I figured out and doesn't matter how hard you are the top side will lose we have 130 mixture has changed only 18%. The sharpness is only 18%. And if you apply the shift, you're going to see that it's not 30x it's still high. How do you introduce it?

The Admin: What the question I'm trying to ask is your kid has crossed 12th class and suddenly you're giving a PhD level books right that doesn't happen if think how the education is also structured 9th is when the difficulty actually starts 9th 10th makes clear you're a math science or commerce person right so then slowly we have the 11th and 12th 11th is harder actually compared to 12th and then you suddenly realize that whatever you learned in the 11th class what we need to have sort of a Warm-up is how much of the overlap is there. This overlap is required to make sure that suddenly you're not shocked, It's a good example would be that you are right now in India and suddenly you're sent to Russia and for the first few days you're struggling what do I speak, how do I speak but if Russian was introduced earlier in your school then you have some idea of how you can actually speak it right?

### 01:55:00

The Admin: So there's a gradual transition that has to happen. You clear on this? You can't just change the bucket. You have to have a gradual transition. You cannot introduce sunscript suddenly and say that start speaking hloka. It has to be gradually increased. And that gradual overlap is also required. So not only you need the band, you need to have a band overlap as So it is not a sharp line here. There's going to be some sort of diffusion of the band B1 and B2 going in also together. And this is a real experience. By the way, I don't have the graph. I should have added that. But in the V4, we saw when we change the band, bof, the loss goes up and down and then suddenly we have to monitor. So in fact, good point. Should have open it. Okay.

The Admin: You see these ups and downs. This is actually what is happening still here, not here. As some of the midstages that you see this up and down, that is exactly where we are struggling on handling that. And a lot of times let me find the exact these ups and downs that you're seeing some of the times here we are seeing that our gradients are jumping.

The Admin: So We need to control this. All of this will come in is about to come in future sessions. Some of this is coming because of Some of this is coming We can control it using this jump. You see that kind of jump happens when we are changing something in the model.

The Admin: This is what I wanted to show but I don't have a full photo of it. I'll find more and share with you. But the point is that the fluctuation that is happening the gap of the fluctuation that is essentially the result of something changing in the model that it doesn't like. So we need to be very very careful with the model that and multiple runs happening at the same time. You can see the average here in both the runs looks sort of similar but the gap that you're seeing how much shuffling is happening is the gradient. We want to maintain that as well. Sometimes the same trajectory is taking us somewhere else and Sometimes it deviate earlier on. All of this has to be controlled while we're training the model. Right here you're seeing the loss. I hope that they could grad that is what I wanted to show You see this norm this is the gradients that going back. On average we need to be somewhere around 0 2\. If you can maintain point to gradient, that you can sleep properly.

The Admin: Initially when start learning is going to start very high but later on needs to get stable and is slowly going up which means model is struggling and you can see that here it stabilizer 35 not a great idea right so all of this is something that we have to discuss we have to get slowly back into right so what I was basically said is that we can't have this sudden shift in the band we have to have a very smooth

The Admin: Otherwise moment you have something like this there's a very high chance the model will deviate suddenly shock s\*\*\* math science that's how you felt in first year in college but suddenly you realize something is damn serious and that happened to me by the way I went to karakpur and suddenly professors was teaching today you're going to learn thermodynamics then the professor sabtach he started Bengali And I was stunned. And then that's where my love for my Bengali friends started. Heart risk. Okay.

The Admin: Yeah, you have a question. Yes sir. Can you please speak in English? Imagine speaking in a class of 400 people requesting the professor. sorry, sorry, Then you'll start a question then look at Bengali tumi tumiki something I don't even remember but what do you think in Bengali and then they'll start discussing in Bengali my pain is your pain now. So here is your long assignment. So this is where your thinking starts. I hope you realize this is the most consequential artifact that we have to design everything else model I'm telling you I've taught it multiple times and you will also get it immediately because now I have so much of background as well. This is the most important decisions of our life for the next four five months. This is going to decide our model is a s\*\* model. It can actually do something in life or it is going to be just one more model that just exists.

### 02:00:00

The Admin: Each one of you is going to draft a mixture of curriculum plan for the V5 as a written specification. I want the plan from you. You can read the whole damn thing. I know you're going to copy paste your cloud anyways, but the idea is that I want full end toend verifiable translated synthetic layer from you. What do you think your plan is going to be? If you were to do this now, benchmarks on everything. How will you come up with this? When are you going to train on a long context? When are you going to train on agent?

The Admin: reason when I going to train on Sanskrit if ever or udu or other languages right so you need to come up with everything now this is important because this is how the evaluation will happen is a subjective evaluation so don't say that I got 200 that don't complain that you will evaluate how well your plan will hold up if a reviewer not me someone from open s of course they will be smiling if you sit around them here data and data curriculum review s across from you and pushed on every number. So the grade rests on the quality of your reasoning and the evidence behind the choice. Why do you think what you have selected to train on comes last and tightly argued short plan is going to score along with the valid earnings or nothing. Basically it earns more points or not. A strong submission gives a defended share of budget to every capability lane and states the index bit across is verified, unverified, translated, synthetic tier whatever you can think of.

The Admin: I wanted to share this because this is what I will be using to evalate Your assignment really is to come back with this. What is inside all of these? When it believe me this you are looking at the opus 5.5 or Opus 1.5 maybe charg 3.5 opus 1.5 might also be better. All right. open for any question you have. What are you submitting by the way? Assemble.

The Admin: GitHub readme it may have your code for calculating something to some sort of script that you may have run anything but I'm looking for a readme link this time not a netly app or widget that link is your definition of how you decided that that's the code you want to and that's the pipeline you want to run on or you want to train on right this is and one thing that I've not mentioned but probably you should think also long context means

The Admin: what that each sample is going to be longer right and this is what we did earlier in our V4 so maybe of interest to you I don't remember exactly so I may be wrong but gives you a general principle so in our case we had a 1 billion which turned out to be 2 billion then we had our 3 billion which turned out to be 5 billion then we had our 5 billion which turned out to be 8 billion and 70 billion was the initial plan which turned out to be forced to be 120 billion so forget all of this we had A, C, model D. Okay, we trained I think till this stage at 4K cuz it was fast. 4,000 words is a lot already. Try writing 4,000. I don't know how many of you would have written 4,000 words thinking yourself, right? 4,000 words is a lot. And then from here to here, we move to 8K, right? So that's how we increase. So if you were to move longer, then you'll have 16\. What is this K?

The Admin: the context length 4,000 12 examples of 496 tokens then 512 examples of 8,000 sequences right and then 512 examples each batch is 16,000 is going outside the screen and came back from here you saw that I can draw around the screen see the 32k then 64k can you see that I can move in 3D 4D so

The Admin: It stopped here. So when you say long context that means that you are doing this you're increasing this. So here when you're discussing long context you need to think about that the token length of each example is increasing. That also a meaning that you need to keep in mind. Right? It's not that the sequence length is 4k. You have a 100k example. You're going to cut it and train it. You've lost the whole memory. So When you say 100k context, you have to train on 100k otherwise you You can prove it but you have to train on long maybe half then proven All Open for questions if any questions.

### 02:05:00

Raj H: So last time we used 20 million or…

Raj H: 40 million tokens. This time we don't say how many millions. In the previous assignment we took 20 million or…

The Admin: I didn't the question between 2.4 to 4 trillion tokens.

Raj H: 40 million to train our data. This time how much you are not specifying right.

The Admin: We'll extend it but you have data set for extension also.

Raj H: right.

Sachin Bharadwaj: So Rowan for the long context part of the curriculum if we train it we have k 4k 8k 16k in order of two and keep up a ratio of the particular long context det in place right is that a good strategy for generalization up to 1 million context.

The Admin: Not possible.

The Admin: Not possible because you cannot have a batch that has a 4K, 8K, 16K example. In a batch all example have same length.

Sachin Bharadwaj: So I'm saying we took the samples up to 2K only and then have a separate batch with 4K only and stuff like that right so is it a better strategy or…

The Admin: Yes. Yes. Yes.

Sachin Bharadwaj: you just okay it will generalize right up until the maximum context

The Admin: camera. There is no shorter one.

kamran shaik: So the shorter ones are going to be padded, in a Okay.

The Admin: Shorter one is a loss of compute for us. So we don't make a shorter one. 5 6 10\. Okay. It's very expensive when you run and…

kamran shaik: So we desperated to have at least 4096\. Okay. Hey,…

The Admin: then you'll see that it'll hurt. Okay, here.

kamran shaik: 

kamran shaik: one more question. Yeah. So, these kind of messages right wherein you have system message role based messages in the context. So those are part of SFT right not pre-training so…

The Admin: I don't get the question.

kamran shaik: wherein we have these role based messages right system user tool assistant etc etc the two and…

The Admin: H correct stage.

kamran shaik: conversation so that kind of conversation is happening in SFT part of pre-training

The Admin: Yeah. Today we discuss two stage four from an to here. So I think harness problem,…

Swati Bansal: Yeah, I mean not related but the issue that happened with open AI's model breaching hugging face from that hacking issue was that a data problem or was that a harness problem because

The Admin: harness problem. so the objective is you tell the LM that given

The Admin: a problem you have to solve it. That is how people train it. They're given a problem you have to solve it. We never add that intuition that if the problem is bordering around nuclear fusion or how to make a nuclear bomb don't work on it because they want it at least the US government to train on it right government to use it or…

The Admin: some people to use it. Then becomes a problem. How to stop it?

Swati Bansal: No, but the…

Swati Bansal: but if you had training examples around reasoning that you got to stop …

Swati Bansal: if based on Okay.

The Admin: that no that's not you can't tell that to a model model does not have a rule book it has a full functioning brain so you can't say for all the problems let's say we say that okay nuclear don't work…

The Admin: what about biological don't work okay what about inciting people towards violence okay don't do that also okay what about asking kids to play blue whale okay don't do it also so the list

The Admin: is just not possible. Can I always come back with a way of getting it to do something wrong?

The Admin: That's why it becomes a harness problem. The harness understands something wrong is happening. Let me solve the models.

### 02:10:00

Swati Bansal: But it was the reasoning that could not be controlled by the harness.

Swati Bansal: Right. God.

The Admin: Reasoning will not be controlled by the harness will see model doing something bad and stop it. That's what there is no way that for example every human has done a mistake even…

Swati Bansal: Mhm. Right,…

The Admin: though we are the most sophisticated em human empathic animals.

Swati Bansal: right, right. Got it.

The Admin: I'm not saying should not be there in the model but I'm saying the hard it's a problem. Harness has to stop it. Si

Swati Bansal: 

Swati Bansal: Okay. Thank you.

Sachin Bharadwaj: So Ron for the opus right we take the previous checkpoint and…

Sachin Bharadwaj: to evaluate the training sample and if you have a large samples to be valued it's costly if you have a large model also to begin with but let's say we distill the model have a smaller one is it a good proxy for the online model that we evaluating right now purpose…

The Admin: Not at all.

Sachin Bharadwaj: because the weights are completely changed tune. Yes.

The Admin: Weights are completely changed. A very different capacity check. Come on.

kamran shaik: Yeah, just reiterating my understanding on the opus. So it's like we have a map of all the weights in that particular model and then we run an algorithmic check whether the back propagation is affecting the same proportionate of the magnitude of weights that it is affecting in the benchmark data set.

kamran shaik: Right. Okay.

The Admin: Correct. Right.

The Admin: So basically let me again reiterate the logic is I have a test. I see my model is good or bad in that is that good and bad is a number which is lost. But inside the model, I find out the important weights that are still bad for that particular benchmark. Now when I'm running test on 124 samples, I see which of those samples are also bad. That is a hint that those examples that are bad for my test are good for training.

kamran shaik: Got it.

The Admin: When I say bad like I meant higher loss here, right?

kamran shaik: I so one more thing you spoke that it is for very expensive for our training cycle…

kamran shaik: but this operation has to be done only once, right? This is filtering of data.

The Admin: No, this has to be done regularly…

The Admin: because Our model was very bad in math benchmark. we fixed it by some opus kept on selecting math examples. Now it is good there but now it is bad in science. Our golden proxy is also changing right.

The Admin: What benchmark it should be good at different stages is changing. So as opus is changing it needs to check the model's current state. Is my model currently bad in science? that is why it's expensive. It has to run regularly if not Once would mean I have the weights of the full life cycle.

kamran shaik: But the data set size that we had originally was fixed at the beginning,…

The Admin: I only have the current weights. I don't know the future weights.

kamran shaik: right? …

The Admin: So yeah,…

kamran shaik: we are going on filtering some portion of the data set at each and every iteration. So, it makes the data set smaller.

The Admin: so that's why have to So let's say we keep the 50% fraction. So now that this means that if you collect one tokens actually only half a tenant token will be trained on not again and…

kamran shaik: But what I'm saying is we are filtering on the same data set again and again, right?

The Admin: You never pick the same batch again, right? You throw that part and…

kamran shaik: Got it.

The Admin: this is the actual Opus paper. their claim is that they get 8x efficiency which means the loss we going to get at 20 billion tokens would have taken 160\.

The Admin: That's why this is amazing and I could see because the total number of tokens we collected around a trillion tokens actual training was 200 and of 200 somewhere on I think 40 or…

The Admin: 50 were let's say 50 of opus 50 to8 it's 400 billion so overall training run that we did was somewhere around half a trillion right and if to get to the same loss otherwise we would have had to train how many 8 into 15 half a trillion tokens All right, guys. I'm going to stop the recording. if you have any questions, I'm still here.

kamran shaik: Jesus Christ.

### Meeting ended after 02:14:50 👋

*This editable transcript was computer generated and might contain errors. People can also change the text after it was created.*

