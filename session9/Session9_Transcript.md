## **ERA V5 Session \- 2026/08/22 06:41 IST \- Transcript**

# **Transcript**

The Admin: All So today's session is going to be on loss function and output heads. But I first wanted to cover this part. This is our I'll say precursor to the paper that we're going to be writing. First of all really good work on assignment seven. this is a problem that I was trying to solve for the last couple of years and I think seven eight of you had I think there are around 10 plus people whose solutions were taken together to solve this particular part. I trained a small model it's a first I trained 40 million and then 100 million parameter model on my Mac and it was proven that this concept chronical front end I wrote there were 10 core problems out of which six were solved by students.

The Admin: I picked them and then worked on top of it to actually get a end to end chroner. So we have a encoder and we have a decoder and after that I also tested something for which I wanted this unique encoder which was to combine words that have never been seen. for example if I were to send this to let's say let's take token you're going to see that it is a combination of four five different tokens so the question was can I compress this into one token and send it and can the model repeat it and even at the 40 million parameter level it was able to do it right so that is a really really good part then we do not have limitation on 32 characters that have not included yet in my own solution but some of the students have suggested that so I'm going to include that as well.

The Admin: So generally if a model has 4,000 dimension and we have let's say 131072 as total number of tokens or vocap we are looking at half a billion parameters right and in case of chrona we have 4 million at the input and somewhere around six or 8 million at the end depending on what is the input size what is the d so these are students we have superhuman then the tata then we have mukund Yaser Swati. So many others are out there but this is a very consolidated report and I want to show you the outut. zero in it. I'll not take you deeper into this because today's class is not about that. But the point is that we are actually beating the baseline which is magical.

The Admin: assume the whole world is using input embeddings and then maybe tide head or lm head and now we have a concept where we don't use both the concepts and we are beating the baseline and that was amazing. this is versus 10\. You can see that for a rank 16 we're going up to it's less number but our main point is our model is half the takes lesser time to train and lesser RAM of course I'm hoping that yes so for example look at this letter we have Z QVX if you were to send this to tokenizer it's going to break that into multiple different tokens right in our case 10 out of 10 we're beating it so our model which is literally at 20 million 40 or 100 let's talk 20 or 40 instance as smallest possible model not trained for a lot. It's trained for probably 20 million tokens only.

The Admin: 1 is to1 not even archentula level but it's able to read that token remember it and actually emit it out and our decoder can use it to get the same token out right so some work is still left for example alpha numeric we're getting nine out of 10 hits for digits and symbols we're getting 9 out of 10 for ordinary English words like archived it's divided into arch and iived right those two words are already seen by the model and it prefers to make a new token using that we can fix In the later test I did fix it but it's really really good results and on the spellings I need to train further but this is one thing where I want really good capacity to be there.

The Admin: So for banana it is saying banana nana just learning and remember it's a very small model train only for probably four five hours rhythm it is going somewhere there strawberry it needs to fix that moment you have strawberry moment our model can spell out strawberry we'll be super happy about that because models generally do not know the spellings of the words they're looking at but our model is going to be the first one where we can do it then we fix it banana we got close to it still and this is based on detentions essentially right

The Admin: How many words can it focus on? Because our model is very small. It's not able to go there. But I think we can beat this spectral part also. Now there are a few other things that I need to work on it. But this is really clear that we have our first paper ready and we can go ahead with a free output head. What this means is that our cap size is not limited anymore. and it poses a question also how do we tokenize now because our model can support every single word possible. Should we actually have a tokenizer or not? So I don't know about the answer to that question but a shortcut says that we will have a tokenizer but while inferencing and while training we will use the combination of making new and sending it but I don't know we need to probably think more about it. some questions on this and then we'll start the session.

### 00:05:00

The Admin: Raj what about for it is using a bit of for…

Raj H: What about four year? Yeah, we can't use it.

The Admin: but for addition multiplication is not compatible with the overall and many of you have done the multiplication addition you have proved it works but you need to prove that model can do it not that a simple function can do And none of you have done that part. You need to train a model and train a model literally is four five hours on Mac today. on Google collab it can also be done for six seven hours for instance. But nobody has proved that a 4 year actually can be learned by the model. I know it learns but proof is there. And my focus was on this because this was something that was wrong pending.

The Admin: 

chirag Tagadiya: how good this is on the math and the coding token I mean so I think one of the problem was to if he's able to handle the coding ol or math symbol is it doing

The Admin: I showed you that moment ago, Nine out of 10\. All right, any other question on this? I'm super happy about it. That's why I'm briefing you on this. A lot of work still pending here. for year also is one of my I say sort of a dream that I really want to get out there. But I've not done tests on it. That's why I'm not excited about it as of now. But if I get time to work on for year, I'll work on that as well. But the main point is that can the model learn to use the foryear. That's the main question. 4 year will work. I have already proven it. A lot of students have proven it.

The Admin: where the main question is that can the model learn to use four years instead of directly this and both are compatible by the way after some thoughts the solution that you have proposed is not compatible but I'm talking about the compatibility is only on a so encoder is already decoder compatibility is currently not there with the four years so if we can fix that and we prove that a model can actually use the 4 years then perfectly fine then we can use any modality for our models which means that we can train on image, text and audio at the same time. today's session it's more like a religious event where I'm speaking and you are listening to me like bud. So unfortunately because a lot to absorb right today's session more on theoretical part.

The Admin: I'm going to try and make sure that you get as much out of it because this is one session where you can link everything that is about to come. it also introduces some concepts which you're not supposed to know right now. So I've mentioned that to be read later on but it's a consolidated state. In future if you ever come back to understanding what loss functions are and where do we use which one this is a session you can come back to. So the session is called loss functions and output heads. we have seen our transform block full end to end. We have only seen the attention part of the transformer layer. We are going to look at the other parts of the transformer layer and then we are going to focus on the loss function and why it matters and what do we add in loss functions, what do we add in loss functions. these are some of the mistakes we have done in V4 while training also and they're costly because you pay for the GPU but if you take care of it initially

The Admin: or at the design stage then we can not spend money that is not required to be spent. So right now that Token is a subword of a big word like transformer. We will not like to store trans. we don't want to store all the words in the dictionary. People do spelling mistakes. new words keep coming up. And if you were to store all the words of all the languages together then we're looking at bill and scale. We don't want that because we have to predict one of the billion which means our output layer to be Input is also going to be massive. So we start with a Token is a subword collection of as many subwords as possible which allow us to combine them and make any word that So we start from there. token is literally a number. for example Tata or Tesla or micro. these might have some number in the overall list. Right?

The Admin: So let's say micro is 40 4,600. We can't send 4,600 to the model and we would like to store some behavior of the token also what does it mean? Micro means small and used in computers and sometime hardware and other details. so we convert that into an embedding which is sort of let's say 4096 or 1024 dimensions. Now each of these dimension if you were to think like humans each of these dimension stores some sort of medium or some sort of detail about that particular Simplest way to think about embedding would be that let's say a man we have a lot of men but let's say we have a man we have a woman then we have a lion and then we have a tiger. Then let's say the first dimension talks about who lives in city. So 1 1 0 and zero right?

### 00:10:00

The Admin: Then second is rsus non-vegetarian. So let's write non-vegetarian. So men are let's say 0.6. Women are let's say 0.6. Lion is definitely 0.9. Tiger is also 0.9. Sometimes they do eat grass and all for their stomach and on Thursday when they have to keep some vat and all so they do eat some vegetarian. what's the walking speed for example or the fastest speed they can run at? So in a scale of 0 to1 right let's say 0.6 women would be 0.5. the reason men run faster from women has nothing to do with physics or physique. It's that they want to run away faster. So they have to put in everything. Lion probably around 0 8\. Tiger would be around 0.9. Right?

The Admin: So you can think that and let's say a weight right will be heavier. So 0.2 lion and tigers are very heavy compared to humans that fire around that. So you can see that for each dimension I'm mentioning some sort of number right then how emotional probably zero women will agree one men will agree let's say 0.5 no nonsense 0.5 something like that okay and do they play cricket and the reason I'm adding cricket you'll understand very very soon do they play cricket yes of course they do then here is zero here is zero okay these are embeddings and as humans we can think of lot of different kind of embeddings but the problem is that our thought process cannot be matched

The Admin: Computer thought process cannot be masked by humans. we are restricted in our own vision on how many things can we think of simultaneously right science says that you can't think of more than three or four things simultaneously. that's the max and computers can. So they can come up with multiple dimensions in which they can fast storing the meaning. the reason I mentioned cricket here is because I want to go back to my example Mahindra Singh This is the basic embedding that will be sent to the model. the moment we say that Dhoni is like a tiger and just like a tiger this tiger is ferocious right and so suddenly we have changed the meaning of tiger there. So in the model all this has to go right and this has to become one change the value basically and this has to become one that is what happens in the transformer but we are on the embedding layer.

The Admin: This is what we want to get or send to the model at least a basic meaning of what the word is without the context right for example black right so what is the basic meaning of black that needs to go right and there are many different meanings of black and one needs to know that basis and after that will keep on changing right these are embeddings as humans we can come up with few of them but you can ask computers to come with 16,000

The Admin: embeddings also right and they have a very weird way of combining different embeddings right if I ask you to count from let's say 0 to 16 you are going to do one two 0 1 2 3 4 5 6 7 8 9 but computers know that if I just use four digits then I can store more detail inside it if I increase this then I can store more right so one 0 0 0 1 can be a big number or small number depending on how it tries to arrange so computers know that we can mix and merge different things and make new things. Humans are really incapable of doing something like that. So some of the embeddings that computers come up with we can't even decipher. We know they get used. We see the examples of and how and where are the getting used and then we can come back and say I think this embedding represents love. But sometimes it might be and dislike and based on negative meanings right u but humans are really really incapable of doing something like this. So where does that take us at the embedding side?

The Admin: So we take a to tokens for example a sentence that the capital of India is New Delhi. So the capital of India is New Delhi. So that is seven tokens and then we will convert them into token ids. So again, We're going to go in the dictionary we're going to see let's say 6,900 capital is somewhere around let's say 6,000 of maybe somewhere around 14 India some other number so we converted that into number we send that number to this embeddings table we go to a table row number 10 and read the embedding and give it to the model here are your seven embeddings right so that's t right and each embedding might have 1024 dimensions or two 2048 dimensions or 4096

### 00:15:00

The Admin: six dimension depending on how rich you are right more the money you have bigger the dimensions you can build and train on D and then we have B which is batch as you know we do not train on one single example if you do train on one single example it's like this you show a computer car or let's a banana and you give an example of banana it will learn how banana looks like then you show apple it's going to say this is not apple this is banana then you're going to say no this is not banana this is apple You show 10 images of apple so it gets better at Next time you show banana it's going to say apple. There's something called not strategic I forgot the word dramat let's use the word called So it has dramatic forgetting capability. Right? I wish humans had that but We remember everything. so we send a bunch of examples so it knows this is how banana, apple, mango all look when I compare them in a single con context concept. Right? That's the batch.

The Admin: We want the batch to be as big as possible because we want to use the GPU together. In general, I told you that the batch which is how many examples we are feeding in and total number of tokens that we send to the model in state-of-the-art model somewhere around a million, right? That would mean that you need 10,000 100,000 million and divide by let's say our context length is somewhere around 409 6ide by two. So 8k something 122\. So we need to send a batch of 122 examples collected together each one of them being 8K that is going inside the model. Now that goes inside transform blocks which we are going to talk about more and finally we have the hidden state. So the task of transformer is to keep on thinking about what is the meaning of this word right? So all of that happened inside the block.

The Admin: But the conversion of all of this into the next token happens inside the last stage which is not shown here which is going to be the main thing that you guys try to solve in the session seven assignment right the decoder part how do we decode listen to the next word so session eight was more about how information is mixed we learned about attention when I'm talking about tiger the model needs to remember that tiger is linked to Tony. So I need to put attention on Tony. So now if you ask me does this tiger play cricket? Yes. has this tiger ever won world cup? Of course it Has nothing to do with tiger but the context links to zoning. That is what attention does. after.

The Admin: We're going to be seeing how do we convert that into a loss. Finally, how do we actually train the model? Where is the loss or value coming from? And the next session is going to be on the gradients and updates and some of the stuff, right? So overall spine is we have a hidden state which is So now we focusing from this part forward that goes to the session seven assignment that you worked on that get converted into logs. what are logs? let us say I have an image of a cat and then I have an image of a dog. And I have written cat here and dog here. What do I send to the computer? I send zero sorry I can't write one.

The Admin: I send one and zero for the cat and zero and one for the dog. Are we clear on this? This is called a one hot vector. Right? So how does the Data set for images is going to look like I have a folder. It should look like a folder also. And inside the folder I have a lot of images and then I'll have a long CSV file where I This is the name of the image and I'll have the one hot vector which is 1 Z for the cat. Then image name here and 01 for the dog and so on. This is the labeled data set that we have. Right? So here we seeing one hot vector. So if this is clear then in case of text right and so one of the things I told you transformer solved or Mr.

The Admin: Savasani solved in 2017 was that The data set itself is labeled. What do you mean with that? So, the capital of India is new Delhi, right? So, when we send the capital of India is we already know the answer, right? So, we do not have to label it. So, we already know the model need to predict new. if we go to our dictionary, to the tokenizer, we're going to see a lot of words and the blah blah blah blah blah.

### 00:20:00

The Admin: Then we have new stored here and then So we have the 0 0 blah blah blah and then we have one here and this is what the model has to predict in our case. Right? So if we have 100,000 tokens in our vocabulary our model has to predict this 99999 times then one and then Are we clear? This is what the model has to models ideal prediction. But we all know this word doesn't exist. So this. Model will predict something like 0.0000001 0 0 0 1 for this I will predict 0.0 maybe negative 0.006 and for this one maybe 0.09

The Admin: 0 9 that's a big number by the way if a model is predicting something like this in 100,000 tokens that's a big number right or maybe it will predicting 0.12 and so on again a very big number you clear on this is one hot vector the one that we want the model to model predicts something like this this is called one hot vector and these are called logits logical bits like what logic the model wants for clear on What is logic? Any question on this? I'm about to hit If I hit the screen will disappear. Q. Okay. So logic that's a prediction heads output right now. And if the vocabulary is big, this number is going to be big. The matrix is going to be a big one. Right? The model hidden dimension till here is let's say 8K. We have to decide 8K, 16K or 4K depending on how much money we have.

The Admin: Once we decide that we have 8096 or I keep forgetting let me calculate 4096 22 8192 8192 8192 okay I not forget 8192 so our model dimension is 8192 and we are predicting 131072 the emitting the total tokens we had so our output head is going to be a billion parameter that is what you have solved in the last session we do not have to have this 1 billion parameter now we have somewhere around 24 million huge saving there but anyways but this is the matrix size that you have to predict

The Admin: That is logic right this is the prediction of what next number should come and as you we're going to talk about that today also one of the most beautiful his station in India is can you please write in chat what is the next token according to you one of the most beautiful hill stations in the country is catastrophic forgetting uti manali

The Admin: That's it only three could okay the reason I ask you to mention all of that is because I don't want to think you also have to think something so we have dling Then we have Miran Muran E. I don't know what that place is. We have Mount Au. My handwriting is bad. Not because I'm a doctor then others also but let's say okay let me write we have aru

The Admin: The reason I ask you to mention all of this is because let's say you ask the neural network LLM train one of the u most beautiful station in India is right. So we have a lot of words. We have Would the model definitely Apple, no. Pakistan, no. Right. So there are many words where the lodges are going to be very close to zero. But there are many words for many cities or places the final lodges are going to be pretty much near to each other. Now after that there's statistics. How much of the world talks about Lin compared to Mat Matan or Mount Auar or Araco right? So this might be 0.01

The Admin: 01 or This might be 0.0965. This might be 0.012. Maybe this might be 0.013 and so on. We clear on this. So there are a lot of words model can predict and none of them are right or wrong because based on the context based on are you from that city based on are you from south or north if you're in north probably you're more aware of north and so on much of that There are far more beautiful hill session in east India but none of you have mentioned that maybe darling will call for that but there are many beautiful there we not aware of them so we don't talk about that so lot of now the world knowledge comes in now the statistics goes inside what these logs actually are right I think you lost the screen right oops one

### 00:25:00

The Admin: Okay.

Umesh Nmenon: Yes.

The Admin: My drawing is there you can't see because I'm not sharing my screen. Can you see now?

Umesh Nmenon: Yes.

The Admin: So now based on statistics these numbers are going to be decided and this is where the temperature comes in. I'm not sure we discussed about temperature or not earlier but some models provide temperature setting like what temperature should in fact we discussed last session this is where temperature comes in now temperature will decide that if you keep a temperature of one actually it's just going to pick araku and say that's it I'm not even going to think if you reduce the temperature then you're giving more options for it to select now it will look at other things and then statistically it's going to divide it probabilities among these words and be greater that's where the creativity part comes in I killed my

The Admin: clear on this.

Shwetha D: Yep.

The Admin: So that is logit for us. but the way I showed you all it Because actual raw numbers coming out of a model that is not what we use for loss that is not what we use for actual temperature also validate. We send the logistics through something called probability or softmax and from there we go to gross cross entropy and complexity and other things come in right and a short note on softmax. So soft max cal online we discussed this little bit in the last session also.

The Admin: So let's say we had these and if we calculate number of three predictions we are seeing that softmax task is to basically create the separation between them right because model inherently cannot create the separation so we use softmax to stretch these numbers small becomes smaller and big becomes bigger but it's based on the amplitude also so three is actually a big number right but if all of them were 0.1 and 3 and 2 same scale but if I calculate logic now you're going to see they're very close to each other right so it does force the model to give a bigger logit because you can see that if it does 0.1 3 and 0 2 the ratios are very close to each other. So the law softmax is basically saying I'm not confident in you saying that a2 is the correct answer. I want that logic value to be also very high. So this is the other side effect of using softmax like we push the model to be very confident on the words it is confident about.

The Admin: But if they happen to be close to each other then this gives a chance for our temperature settings to come in and then use some of these words right. So it works in both the Cross entropy we have a topic pillow. So we're going to talk about that. Publicity is the inverse of probability. if the probability of something happening for example yesterday India beat Pakistan 5 is to three in hockey right? Is that a surprise to you? If India was a really really bad team in hockey and then they did beat Pakistan, it's going to be a big surprise, So let's change it? What is the probability of Bangladesh beating America in football? Their football anyone can you come up with a big number or small number?

Raj H: It's The head.

The Admin: Don't say zero. I need to do some math. It will give me infinite number. Zero.

Satyanarayana Murthy Toleti: 01

The Admin: Thank you. So let's say 5% 01\. So right that's Publicity is reverse of that and it's derived from the probability. There's a formula I'm going to show you. But formula is not Interesting is the Surprise is literally reverse of probability. So if Bangladesh does beat America in Chicago and in football then you are heavily surprised. You are stunned what just happened and that comes from the low probability. So when anybody gets surprised when you do something and they get angry tell them don't be angry this probability was very low and that probability happen right so now something that you can tell your wife and you'll be safe for that day I don't know what will happen but you can try and use that that that's essential perplexity right

### 00:30:00

The Admin: So it's a surprise how much information this event has given me. And we're also going to discuss residual streams and ffn and swig loop because we just let the last time we showed you the architecture of a transformer block and had a lot of things attention and the stuff we only discussed attention. We did not discuss resolute stream figloo rms norm porm so many different things right so many different words coming together. But once you take off all the marketing or gate not gate GRE and GMAT stuff out you're going to see they are very simple things and there's logic behind why do we do them right and that's what we're going to discuss about in today's session this is how a single transformer block looks like we have X which is a token coming in then we have this thing called RMS norm which is normalization of a certain kind what is it we're going to discuss today then we have attention the block we discussed in last session all that gets

The Admin: added H. if I think about it, what is there on the screen? Because this is the block and I want you to carefully see Which color should I use? This one. Okay. If you don't the color, don't blame me. You only told me to use a color. If I see what is happening if my pen is not working? One second. Yeah, now it's working. So I wanted to see that X here goes here. That is how I want you to see. something gets added to X and then it goes Something again gets added to X and then goes out. Do you see that? Can you see the screen as I explained to you?

The Admin: This is the concept coming from Resnet is one of the brilliant model that was invented by Microsoft and what ResNet does is so before ResNet u I wish I could teach convolutional neural networks to you the brillian networks and I can't tell you how much I love them but I can't cuz it's 11 course anyways. So we let me still take a small detour. I'll try and finish in 2 minutes. I'll speak very fast. There was a time before 20 2012 when the whole world was built with engineers who are doing feature engineering. The task in feature engineering was to design features. So if I were to design a circle, I'm going to write some sort of ma mathematical algorithm to detect a circle. And we were really good at it. But the problem is that I can only detect a circle of a certain size. So if the circle was small, I If the circle was bigger, I have to write a new detector. If a circle is slightly oval, my algorithm will fail. So I write old detector. But if oval was this shape, I'll write this detector.

The Admin: If the oval was this shape, I'll write this detector. If the circle was not finished, I'm stuck. I have to write something else. If the oval is not finished, I'm stuck. If I have to calculate this and the oval, then I can't work on it. You understand? Future engineering difficult. And we have to come up with all these things. Then in 2012, there's a guy called Alex. I don't know do not know second name is more interesting than the first name. I think it's called Kruski in search online. Alex came up with the idea that new networks are there. we can solve this by new network. But the problem is we had one GPU and we had teeny tiny RAM inside it. So we thought why don't I take more GPUs and connect those teeny tiny RAMs such that they become slightly bigger RAM.

The Admin: That is literally his contribution. He was the guy who actually connected all the GPUs and trained the world that you can connect GPUs and train a new network and then train it. So before that in 2010 there was a competition called imageet which was for finding these features of finding cars and telling whether the image is a cat or a dog or a car aircraft. Before that in the first year In the second year 2011 the feature engineing won new networks are here. in 2012 when Alex made this feature was here and neural networks were here and we won. Since then all the feature engineers they died not died but you get the point right. So feature engineing died. So this is what his contribution was and before that we had architectures which would look like this.

The Admin: We have a convolution block of 3 \+ 3 which gets added with a 5 \+ 5 block and after that we combine them and then we write a convolution of 7 \+ 7\. These are the kernel size how big features we are trying to find. And after that we split that into 3 \+ 3 and then 1 \+ 1 and this is what my Google was doing. Then I'll have a 5 \+ 5 also why don't we put a 7 \+ 7 as well and let me repeat this two times and after that I'm going to add a 3 \+ 3 and 5 \+ 5 and 1 \+ 1 with a slide of two and 3 \+ 3 with a slide of two and so on. This is what Google was doing, Google is a Randomly searching different kernels and then putting them together to make something. Then came Bajigar and is one of the favorite network. It's called a Bajigar network. the year is 12 2013 or 14 I don't remember. I think It's called VGG. they came up with a very simple architecture. They said I do not need all of this crap. I'm just going to go with 3 \+ 3\.

### 00:35:00

The Admin: So every single convolution layer is a The feature size they're trying to find is three cross and they were second right Google beat them because they were searching for better kernels. this is Nobody knows remember this architecture. Everyone remembers VG because they came up with a very simple architecture. Next year which is probably 2014 and 15 Microsoft came in and they did something that has never been done before and since 2014 every single architecture including transformer is using it. See what the first architecture was and this is important in the VG we had data coming from here then goes to the next layer data goes to the next layer we process it and finally we have a large prediction layer let's say call this head and then we have predictions here Microsoft said This

The Admin: This is my image. This is my prediction head straight line. And I'm going to slowly change it. All the processing is going to happen here. So this architecture shown like this which is a design I hate because both of them give you a very different idea. This is In resonant we have a single line of communication from the image till the loss and anything that we change on the data happens outside and then we add to the image.

The Admin: Just on the image, a very simple example of that would be you take a image of a cat, you start blurring out everything that is around it. You just show the cat, right? Half the problem is solved because if I want to learn a cat versus dog, I also have to learn the texture of horse because horse is not a dog. I have to learn how the road looks like because road is not a dog. I have to delete it. Just to say there's a cat or a dog, I have to undo a lot of stuff in the image. I have to get rid of all the stuff that is there to be able to say it's a cat or a dog. And in this architecture we are slowly blurring that out. Very good way of understanding what the residual connections do So all of these are actually blurring them out highlighting cat highlighting dog highlighting some of the features that might be missing. And then finally when it goes to the prediction head we know that it's a cat or a dog. Another advantage is the loss propagates like this. So if a loss is going like this I can hit any layer even if this layer is not working properly. Right?

The Admin: I have a direct stream of my loss through the third layer or any layer of my choice. This is called a residual connection. These are called the residues that are being added. That's why it's called res net residual network, right? One of the building architecture that was invented. And we see the same line here. This is the line that is there and these are residues that we are adding. Right? So every single time we are doing something, what are we doing in transformer block or whole architecture?

The Admin: We have a token for tiger. It has flesh eating and animal and 400 kg and so Suddenly dhi came into picture. All of that has to be forgotten because you might say what is the weight of this tiger? You have to say 100 kg or 92\. I don't know. All the stuff has to be removed. This is where the removal is happening. Right? That is what this resent connection is. keep that in mind. Here I mentioned also mathematically we have x which is equal to x plus attention So we adding some stuff to x, right? And that plus one is zero, right? 1 \+ \- 1 is 0\. So that plus doesn't mean necessarily we're adding. We might be subtracting the editive attention part also. then we have this feed forward network. I think I should drawn I have drawn it. Yeah, I'm a good guy. do you see this let me show it to you how other people show you otherwise you can just say transformer architecture decoder.

The Admin: Let's open any image of our choice. Let's open this The image designed by the first paper and nobody has stop using it. this is the block that we are looking at. That's why I don't want to show it to you because it's wrong. Yes, this is the correct one. Okay. Can you see the decoder architecture? Do you see text and positions coming in? You see the self attention and you see the wrong way in which we design. This is the way we design because we want to show this part not the But for me the line is more important. Attention we discussed already layer. Now about to discuss. Then we have this feed forward.

The Admin: Do you see this feed forward? This is repeated 12 times in this particular model. Maybe repeat it 100 times depending on the model architecture. But this thing is the block. This is called a transformer layer. Are we clear on this? Yes. No. bs up, thumbs down. we discussed in the last session. we are about to discuss and I'm about to explain what is this feed forward doing. Right. After that we again have a norm and then go out. That is this FFN we talking about right? So it is listing with that line. FFN inside is very interesting. In FFN we have something going in. We do up projection then we do nonlinearity and then we do down projection. Right? So instead of showing you this let me draw it.

### 00:40:00

The Admin: So if you remember we have 4 096 embeddings for the token coming inside a transform block right and if it goes inside the first thing that happens is the self attention. So sorry the MSA multi retention and the stuff. So let's just write attention here it's trying to focus on which token should it also focus on and updates itself. After that we have something called norm happening layer norm RS norm we're going to discuss that but after that we have this FFN block right in the FFN 496 we looked at something called up projection this is going to become four times its size it's going to become 16k then we're going to add nonlinearity remember first session number one and two discuss we do not add nonlinearity you cannot learn so this is the layer that is actually deciding

The Admin: this value should go low, this value should not go at all and so on. And after that we compress it back to 4K. We again add some sort of this layer which is our layer norm. And after that we have again 4096 coming out. Right? So this is little expansion working on something compressing it and checking it out. Expansion helps looking in much more details. If I have 10 books and I want to figure out where should I keep them, I have to open them. I have to understand what is inside. Then I have to record that and then I have to close it and give it back because I got 10 books. I have to give 10 books back. We're just able to classify

The Admin: them I need to be able to expand them properly. So 4096 books concepts embeddings are coming in. We're going to expand that Why four? Because the first paper used four after that everyone is using Chinese have tried a lot of numbers. They've gone down to 0.25 also which is something we did to save money how many books you want to see. You just look at the label and you can look at the label also and say right that this is a geometry book or this is a microbiology book. We don't get to very well defined a microbiology book written in 1960s obsolete should not be part of all that stuff we can't do if we compress this but if we were to expand which is what all the modern state-of-the-art big networks do then we can get deeper inside those logics and arrange them better and the final output is 4K because the next layer is expecting 4K right so we have a 4K for the embedding token goes inside one block then we have second block this expecting 4K so output of this also has to be 4K right that's why we have this compression

The Admin: also so this is the main block where the actual learning happens right so this is what is written HD the dimension of a token or token going in 4,000 dimension up projection somewhere around four times so four 4k becomes 16k now I'm working on it we add nonlinearity aloo be pou can be and many such and then we have down projection reducing back to 4k and then feeding it to next layer are we clear on Any question on this feed forward network? We have Ganesh Ganesh.

Ganeshkumar Chandrasekaran: Robin can you just scroll down a little bit or for scroll that attention the previous screen? Yeah. don't have a basic doubt.

Ganeshkumar Chandrasekaran: After attention we found out that how each word compares itself with other word. We got that score.

The Admin: Yeah, reverse.

Ganeshkumar Chandrasekaran: Then to that score we are adding the embedding. Am I right? So intuitively what it means.

The Admin: As I said, that is how world to words want you to see what is it that I want to see. I have the word going attention looked at other words and…

Ganeshkumar Chandrasekaran: Yes. Okay.

The Admin: figured out these things should be changed and I made that change in that plus different way right I went to a school and school fixed me versus this is what I am and school added some properties of

Ganeshkumar Chandrasekaran: So then in feed forward network what happens now it is So based on other words it is switched down. So now the feed forward network intuitively what happens there?

The Admin: Yeah. So in X right now I'm changed based on…

Ganeshkumar Chandrasekaran: I understand we upgrade down that type but what intuitively happens there?

The Admin: what other embeddings want me to So the first part is my interaction with others.

Ganeshkumar Chandrasekaran: Yes. Yes.

The Admin: Social media. What's app, telegram, Instagram. Now the second part is going home and reflecting do I even have that kind of money to buy a Ferrari like I show I saw in the photo of my friend can I go to Paris tomorrow because I have to go to job that the self reflection part where the reality hits where it's saying you want me to have this much high number for Dhoni on cricket but I also have all these properties of tiger I need to get rid of them.

### 00:45:00

The Admin: So that selfcorrection happens in the FFN part.

Ganeshkumar Chandrasekaran: Okay. Okay. I get it.

The Admin: Okay. Right.

Ganeshkumar Chandrasekaran: That's it.

The Admin: We have question a lot.

Ganeshkumar Chandrasekaran: It's only

Sachin Bharadwaj: Rohan, I was thinking does this order matters? I mean, can FFM come?

The Admin: A lot.

Sachin Bharadwaj: Okay.

The Admin: Link it to your life. So you talk to yourself. I don't have money. I'm struggling at my job. home is always panicky. my wife or husband not beats me but fights with me.

The Admin: I have four kids I have to take care of there's school fees spending then you go on Instagram and then you see Paris I'm going to go based on that if you decide tomorrow I'm going to go to Paris I'm going to destroy everything so what do we do we wake up in the morning we look at Instagram first to make sure that all that thing that we can't do we have seen and…

Sachin Bharadwaj: Okay, thanks.

The Admin: then the life comes in which is the job and the actual life if reversal is going to be nightmare you're going to go to your boss and going to say send him to Paris right so People have tried the reverse part but this architecture has worked better. So we have a statistical proof that this is the best one. Now this nonlinearity is a very interesting beast here. Generally the nonlinearity you guys are aware of or may be aware of is something like relu right? Reu is rectified linear unit which means that if something comes in we decide if it is positive we let the number go if it is negative we make it zero right?

The Admin: some sort of nonlinearity curves that we have but we use something called swigloo. Sigloo is slightly different right in swigloo this is how RLU looks like relu is weight comes in we add ro and then weight goes out I will have to draw here to experiment further so let's say the weights were wrong color yeah let's say the weights were \-1 0 2 3 \-

The Admin: 4 it Rail is going to convert that into 0 0 2 3 and 0\. You clear on this? The way it's going here are The way it's coming out from here are these. data value here. That's how it works. And After that we have Swigloo is not a replacement of ReLU. You can see that architecture itself Sugi is more like if you are exposed to RNNs and LSTMs and GRUs of old era

The Admin: of 20 pre20 2016 it's similar to that actually so we do not have one weight here if you decide to use swigloo first of all you're not going to say that I'm using something like relu you have to say I'm using a design pattern relu is a concept of adding activation right what activation I'm adding so it's or it is glue or some others there are many different variants for that switch for example is a replacement of ru Right. Swiss is one. So RLU is simply like everything negative zero and Swiss is more like how humans think. somehow this is very similar to how humans have the processing of neurons that we have a graph similar to that right. So This is RLU. So Swiss is comparable to ReLU. This is called Swigloo is architectural concept. Swigloo is a design pattern.

The Admin: If you decide to use swigloop, you are not going to have W1, but you are going to have W1 and V. So you have to first have two neuronet networks for swigloo concept to work. Then one of the weights inside is going to go to a Swiss which is a slightly different variant of RLU and we have it also going through V and both of them are going to be merged here and then it's going to go to W. After that what you can do whatever you want to do. So my first question to you are you clear that swigloo is not a replacement of relu it is actually a design concept it's a design pattern right the first thing I want you to notice second is when you say that you're going to be using swigloo you are actually changing the architecture sugl is a design concept we have to change the architecture to be able to use sugloo concept okay so here we are going to have two layers W1 and V1 is going to go through activation and V is going to go with some modification

The Admin: So why are we doing it? here we have The concept of What is a in computer science or in electronics the gates are some things that allow other things to pass. Right? So we have this data coming in and this data is 0 1 0.3 0.2

### 00:50:00

The Admin: two, three and four. Right? So it goes to a gate and gate decides that I want these values to be kept. Are we clear on this? So we have 1 2 3 4 5 6 1 2 3 4 5 6\. Nothing is here. So gate says these are the values I want to keep. Say yes or no. Hands down. The other layer decides how much of it to keep. So, it's going to multiply this by let's say one

The Admin: this by two, this by zero, this by let's say three, this by 0 and this by three. Okay, so we multiply that and let's see what do we get. We get 1 into 0 0 then we get 2, then we get 0, then we get 0.6, then we get 0 and then we get 12\. So normally and then we multiply both of them. if you multiply both of them, what are you going to get? You're going to get zero, you're going to get two, you're going to get zero, you're going to get 0.6 is retained, then you're going to get zero, and then you're going to get 12\. This is the architecture of Siglo. So you can see the nonlinearity, but you can see a scale also, So not only this block allows us to say that this dimension is important for me, I'm going to take it forward. It also decides this dimension is not at all important for me. I'm talking about Singh Dhoni.

The Admin: Why am I talking about my canine teeth and that I have four legs and then I have sex in desert in forest and all that is not important for me. This tiger is mandhi. So I have to have all the concepts of cricket and world cup and taking roles in advertisement and I earn crores of money and so That is a simply gate that helps in doing this further. So attention allows us to learn from other word what am I the self-reflection happens in the FFN block where the word looks at itself and says that okay I still have features left of animal not the movie the tiger right so I need to get rid of all of that and it basically does it like this if I was to use simple rail and all then if we are forcing the neural network to actually add positive values which are my positive traits and add negative values so can remove it but that destroys the performance of a new network

The Admin: Because sometimes They are my negative values. For example, I do carry hate, I do not want to justify the whole world between zero and one where zero is hate and one is love. I like to have minus1 to \+ one. Minus one is a pure hate, zero is neutral and then one is pure love. So this is what allows the new network to do something like that. Okay, we have another this is coming from new network.

Anirudh narla: Sir what exactly does negative represent here?

The Admin: So negative basically I just said plus one is love negative one is hate. So on 6 this is my feelings for you not really but my feelings are positive but you understand the point. Got it?

Anirudh narla: Yes, somewhat.

The Admin: One second.

Kunal Sinha: Yeah. here we are seeing that W2 or something is related with W1. So in back propagation no I like in the switch case W1 V is also related to W2 right.

The Admin: Where do I see that? How Matrix multiplication.

Kunal Sinha: you have W1 and V coming. Then there is one after the switch block there's W2 coming there.

The Admin: Matrix multiplication. Correct. Yes.

Kunal Sinha: So back propagation do we have that partial derivative still there or…

The Admin: Of course.

Kunal Sinha: will that be different?

The Admin: Of course it's It's a part of the graph.

Kunal Sinha: Okay. Okay.

The Admin: So that's Swiss.

The Admin: But one question that should come to your mind because it came to my mind and it has not come to your mind and you're not ask me so I'm angry at you is that this looks like we are increasing weights. Yes. No. Why have you not asked this? So you claim to be doing some super interesting research. You did not think of it.

Soma Korada: increase weights. Yeah, it does.

The Admin: Why did I ask this is…

Soma Korada: I had a question not really on increasing weights but Swiss W1 looks similar to one of the relus also has that pattern, not really making all your negatives zero but have that little variation.

### 00:55:00

Soma Korada: I thought it is similar but then V was a different thing in this architecture. bringing in that magnitude or I missed asking

The Admin: what happens when people do They answer something else. So My question is why have you asked me that this looks like more weights and Saturday morning you just woke up why would you ask? Anyways, so it does not increase weights because what we do here is we try and reduce some of the dimensions of W. So we can compensate by V, So we are trying to optimize there. so if you were to check a new network it will come very very close, So we'll have two cross this number and 1 three but here we'll have three cross four number and something like that. So we try and compensate when we using SWLU and that is what helps us. We're clear on this. So it does not increase weight.

The Admin: It can increase weight if you're blind but if you use Swiss we are careful in making sure that we drop some of the parameters or multipliers inside to make sure that both of them have equalish weight. let's come on I did make a really beautiful widget for RMS but there's a video that is even better. So I would rather show you that instead of me failing to recreate it and I'll not let the whole video play but okay even before this happens I need to explain something else to for that I need this not even drawing. Okay. 1.001 is it a big number or small number?

The Admin: Anyone? Okay.

chirag Tagadiya: It depends on two to other number right to which you are comparing on I mean I mean yeah it's close…

The Admin: Compared to 0.99 Close.

chirag Tagadiya: but there are infinity many numbers in between that as well…

The Admin: I'm about to multiply them with the similar numbers now.

chirag Tagadiya: if you're talking about No,…

The Admin: Are the good are they closed? Okay, let's so I want to multiply it with itself 1.01 and…

chirag Tagadiya: it will be

The Admin: you see that the effect is not much it just became 1.002 but I want to do it million times a lot of times because that's what is going to happen inside Same number is going to be multiplied again and again and again with other numbers. So let's say we go to 10 became 1.01. What if it was 100 1.1? 000 2.7? What if it was 10,000 21,000? What if it was 1 million? My calculator is not keeping up. let me add one more zero. It's still 2.22,000.

The Admin: Right now if I add one more zero because it does happen but a same number will get multi carried forward millions of times and billions of calculations will happen because we have attention for each word each token and can imagine how big it can become are we clear on this just the effect of that number now I'm going to just do this 0.99 and doesn't matter how many times you multiply it will always be less than one in fact it will get close to zero

The Admin: And I can increase this precision. I'm increasing the precision right now to get back to my number. Look at how precise I have to be. But if I keep on increasing it on other side, you see that it becomes smaller and smaller. What I'm trying to say is if you do not bind the numbers between positive and negative 1 in a neural network because we multiply a number so many times it explodes and we cannot have an exploding number then we cannot compare a 0.1 number with a 10 million number. the scales are just drastically different. So we try and compress everything between plus one and minus one. Are we clear on this? We want every single number in a new network to be plus one and minus one. what happens Multiplication is what is causing this explosion. Are we clear? So whenever you are seeing a matrix multiplication which is a weight which is a linear layer or any layer that has a matrix which is going to multiply the input weights coming in, you're immediately going to see a norm after that.

The Admin: something that normalizes it. And if you were to believe me then you learn everything but you don't. multiplication layer norm. You will not find a single neural network where you will not see a norm after some sort of multiplication. You will see if you go to old concepts before 2014 layer normalization and bass normalization all of that are recent concepts. Bass normalization in fact is a 2015 concept came after renity. So 2015 sounds very old 12 years ago but these are not very very old concepts. These are still modern concepts So every time we do a matrix multiplication for input coming in we have to add a linear layer some sort of normalization layer and now we have a layer norm and then we have a RMS norm.

### 01:00:00

The Admin: So I'll let this video play and for that I'm going to first stop sharing my screen and then I'm going to share just that screen so you can hear the audio also. It's a two-minute video with no ads I promise. Deep within the neural network, raw activations are chaotic. A cloud of data drifting with bias and unknown scale enter layer normalization. It forcefully centers the cloud, scrubbing away the bias. Then it scales everything to a standard size, perfect for finding patterns hidden in the noise.

The Admin: Meet RMS norm. It doesn't care about the center. It simply projects the energy directly onto the surface. No centering, just pure efficiency. Fast and effective. Are we clear guys? That's all I wanted to show you. It's a two-minute video, but for me, the first 30 seconds matter. Let me go to the whole screen now. So, RMS norm is going to take us to this position, right? where it forces everyone to be that on that one scale.

The Admin: 

The Admin: Below whereas layer norm which is what people used to use earlier we'll try and push it somewhere around a scale he mentioned about the scale but that scale is also one for us but here we do not have a lot of guarantee that everyone will be around that part right but layer RMS is going to push everything in one everything in one you might see that then everything is one then how do I look at and you're seeing 2D also so don't get confused right your networks have 4096 dimensions 9,000 8,000 dimensions 16,000 dimensions this is a 2D represent

The Admin: presentation of that. because we can't see 4D so we have to compress them in the overall screen to show in 2D. So when we say that we are doing something like this in RMS norm and it's pushing at one axis it's a square plus b square and a dimension first b is a 16 dimension c is a third dimension a square b square c and then 496 dimension all put together equal to one. So that 4,96 dimension it is landing on a sphere of radius 1\. Clear on this not that one dimension has become one. So that is what RMSS norm does and then you can imagine that how beautiful this is because now inherently using mathematics we are forcing everyone to be around one and The reason normalization does not destroy data is because we do the same thing for everyone and we can reverse it.

The Admin: So if something can be reversed and we can get the same number back, we're not destroying So we have layer norm and we have ROS Clear on it formulas and all. You can look at it. It's very easy to understand. Layer norm is basically taking all the numbers. Let's say we have 14 numbers. We want to normalize them. We're going to calculate a mean of that. We're going to subtract a mean from each number. Then we're going to divide it by the standard deviation. That gets you the number that is normalized for that doesn't really take care of the dimensions inside being there but RMS norm allows us to do that. Then we have a prenor and then we have postnorm. So before 2017 people were using prenom and after 2017 postnorm and after 2017 we are using prenom. here I would like you like to take you to net again v1 versus v2. I'm hoping somebody has still left that image.

The Admin: So here we have resonate V1 on the left and res V2 on the right. The resonate is what connection The residual connection that is coming in and what you can see is that we are adding it here and then we have a ru here and then we are coming here. Right? What did we discuss? We discussed that the residual line must be unobstructed. We can add to it but we cannot do any operations on top of it. This is not allowed and that is exactly what we're doing here. We're adding an activation on top of the residual line. That's the only fix that happened here. We do not have that activation here. Are we clear? Of course, this looks complicated and the relu has gone inside. That's why we calling B and Re and all. But that's all we have done and that is exactly what we did in 2017\. So we learned in 2015 to not do it.

The Admin: Then we made our new networks and transforms 2017 2018 and then again we went to our old memory and then fix it later on. That is exactly what pom does which is basically taking that attention or normalization out of the residual stream and does it in the block. So now you're only aware of the pom postnorm you're never seeing because I've not tried not to show that to this is the block overall block. So in a block we have attention we have KQV and then we have output. So we have four neural networks there and it costs some around 67 million. Then we have FFN swigloo model. There we have 3 496 and gross 11,000. 11,000 is a 3x or 2\. I told you that we do x In FFN we take one model make 4x and then compress 4x. If you're using swigloo, we don't do 4x. We do something like 3x or 2.7x. Why?

### 01:05:00

The Admin: because Sudlu adds one more model inside it to contain the cost and that is around 135 million And then we have two normalization layer which will have some of its own parameter. So each block of transformer on 4096 architecture is going to cost somewhere around 202 million is around 2.2 billion into let's say we use a 48 layer network. Here we're talking about 4.7 billion parameter. plus 131072 into 4096 divid by 10 million 100 million billion. Yes.

The Admin: So we're adding a billion parameter here plus billion parameter on the LM head. So overall this is around 11 billion parameter model. So that's how essentially we decide. output head we are sending in 4096 that needs to now span into 131072 right and becomes logit. So that is exactly what is shown here. So nothing special here. this is And then we have other idea weight time which we also introduced earlier where we have the same matrix in reverse. in input layer hot vector comes in right. Cat example goes inside the model. What does the cat go inside the model? Cat is 00 1 0 0 goes to the embedding layer zero not required zero not required one. I need to read that 4096 number. So out of 131076 hot vector.

The Admin: Third vector was one which is cat. Talks to this particular matrix gets that input dimension which is 4096 and sends it to the model. What happens in the output head? 4096 hidden dimension is going to this matrix and from there it needs to convert into cat or dog whatever it wants to predict. So the reverse happens there. So in weight time for smaller models as we discussed we can use one as the reverse of the other. But in bigger models which we are going to train we don't do it. That is the conceptual meaning that we already discussed earlier. Right now let's look at this.

The Admin: We have the Output head is going to be H which is the hidden vector coming in. And then we have W which is the output head matrix the final layer. the cat sat on the mat has to be high. now it's not because we are showing a untrained neural network. But this is how the model cts. Are we clear on this? We have a vocabulary of 12\. We can only predict 12 words and we have eight dimensions. So we have 1 2 3 4 5 6 7 8 dimensions here. What is based on this design? This is What the size of this LM head? Can you count how many of these columns are there?

Syed Abdul: 8 \+ 2

The Admin: 8 cross rows that is size of the element.

The Admin: This is eight. What? Dimensions we discussed. We may have 4 0 96 dimensions. Right? We are showing eight. Why? Because my screen is not big. 102\. This is the vocabulary for this widget. What is our vocabulary? 1 3 1 072\. Right? So cross 1 3 1 072\. Half a billion parameters. Are we clear? But this is how the output looks like. Yes or no? Okay.

The Admin: The dog ran across the floor mat table something has predicted here right she put it on the sat mat a cat what is it predicting it's predicting right now which is the highest one 16 sat it's predicting the cat sat on what is it predicting it right now predicting dog right it happened then it is predicting so based on the next word these numbers are going to change as we train them numbers are going to become better and this is the logic that we get and

The Admin: where we had soft max on top. this is an important point that you need to remember. Scores are not probabilities. The model is not predicting probability. The model is predicting the statistical view of the world that after the world says this word should come in. We convert that into probability. So the logic for Delhi, Mumbai, Chennai, banana runs might be something like 2 1.5 minus one minus 1.5 what the model predicts. We want probability distribution. We are going to convert that into probability. So we add a soft max on top. Soft max is going to look something like this. Now we've never looked at the formula of soft max but it's not difficult. We're going to take 1\. exponential of 1.0 exponential of 0.5 plus exponential of 1.0 plus exponential of 2\.

### 01:10:00

The Admin: And if you're calculating soft max for daily put exponential of two that's why summation is sum of all the expo all the logs on top of that exponential of that logic very simple formula right and that's how we calculate soft max what will softax do for 2151.5 let's check that what will sockmax do

The Admin: for how many other 1 2 3 4 5 2 1.5 \- 1 1.5 so this is going to be two going to be one so was there a zero anywhere no 2 1.5 sorry 2 1.5 negative 1.5 Five. Right. So, right now it's going to go with two with a number of.56. That's a soft max that we're calculating. Hands up. Bad. Smiley.

Syed Abdul: I have a Why?

The Admin: Go ahead it's not about picking up it's about penalizing…

Syed Abdul: I understand it's converting to a probability distribution but we can still see that two is the So we can still from this logit itself pick up the highest number or whatever.

The Admin: which is what I'm going to show next but since you've asked here let me tell here only this is a good screen to explain okay What is it that We want the model to predict 0 in this specific case 1 comma 0 comma 0\. Correct? But…

Syed Abdul: Yes. Yeah.

The Admin: if you take this to predict, you're going to see that we have a big mismatch. Models are really bad in predicting zero or predicting accurate number that you want. You run this.

The Admin: we convert that into softmax and then we get this and…

The Admin: then we compare it with 1 0 0 0 and 0\. So soft max is not for that we don't know the highest value. soft max has to tell the model dude I want you to I'm okay as long as you're predicting this no problem but I want this to be one can I do something about it model will go back and say what can I do can I predict it to be 20 right or I went to a direct number directly but how it learns I'm predicting 10 it's going to come back and say h okay good enough so 0.9 is good but if I predicting let's say six and we getting something like it is also good four dude I'm

Syed Abdul: Okay.

Syed Abdul: Why not just normal normalization like one by sum of all the numbers that would also convert it to 1, right?

The Admin: not happy it's 0 91 it's like a parent who said udith that you're scoring 91 only in your CBSC can you please score 96 look at the shamaik uncle maybe right uncle kavita so something like that is happening here there no try doing that

The Admin: because I did explain to you right 1 2 3 and 6 see that whereas same relative amplitudes big difference and what did I say every time you see linear layer or…

The Admin: a multip matrix we add a norm layer on top of it. Did I say that? Yes or no? Did I say that every time you see a linear layer or matrix multiplication you see a normalization layer on top.

Syed Abdul: Can you repeat?

Syed Abdul: Yeah. Yes. No.

The Admin: Do you see that on top of linear layer here? Precisely for that reason here we do not want normalization.

The Admin: This is all the details going inside your networks and your network finally deciding I want this. And if you not normalize what it decides, you have just made all the details small. The decision is not equal. Decisions are Clear? All right.

### 01:15:00

Syed Abdul: Yes.

The Admin: So we convert that into softmax. So here again the same softmax calcation is shown. surprise surprise is essentially the publicity and that is negative log P. So after you calculate probability which is let's say 1 by,000. If you calculate a surprise of it which is a negative log P you're going to get 6.9 and if you see two independent events and they are at 1 divid 1 million and surprise of that is going to be 13.8

The Admin: eight the surprise number and surprise number is very difficult right so people came up with this even complex word called perplexity let's call surprise in mathematics as perlexity exactly the same thing right so when you use complexity the app I'm talking about you get surprised it's so good and then later on you realize it's only using openi at the back end so it's still a surprise still perplexity so they're truth to their word so there is perplexity are we clear on Okay, also I explained this I have not explained and it's slightly complex version. So I will take some time in explaining this. no first I have to show you the screen because If I wrote it then you should also read it. Why should I spend time in writing and you not reading?

The Admin: You also should have to go through the same theme. Okay, we are about to discuss cross entropy. we use something called cross entropy. First, I've explained the surprise part to you that table that I already showed you. Now, we're talking about a general version. What this Can you please all read without unmuting yourself? Can you all say used in model distillation together with me? used in model distillation. We are not doing model distillation in the course also. We may not do model distillation but it's a very good way of understanding what I'm about to explain and you can do model distillation but we are not going to tell anyone that we will do model distillation this time. But what is Model distillation is essentially we make our model behave similar to cloud.

The Admin: I want to show you one image which is a open source AI model compared to close gap. This is model distillation in front of you. This is the one I want to show No latest I want. Where are we in We are in 2026 and Google still can't give me the correct results. Yeah, 24\. Really? Okay.

The Admin: tools time last month. Thank you. I don't get those clouds maybe here people will post old images. finally something worth looking at open image and we go here. Okay, this is distillation in front of you, but they're not showing all the models properly anyways. But you see this gap is a distillation gap. What China is doing is brilliant. They're letting OpenAI and Microsoft and Nvidia and Meta and especially Anthropic train whatever they want. Once they have trained it, you somehow try and understand what is it that they predict.

The Admin: If you understand what is that that they predict for a particular word, you just need to get that information to improve your model and your model behaves like them. And that's why the gap is changing very very fast. I'm not sure if you have seen I'm using this model by the way. I'm just very very happy with how this is actually behaving. This Quinn 3.827D 2017 very small model but look at they're comparing it to open OPUS 4.6

The Admin: max that was literally I think January or October last year and not far off some places is actually beating it also and 27 billion this is a trillion parameter model of course it will not have as much memory as much world knowledge but it's going to be really good in coding because that's what they focus on right so the concept we discussing is that concept context or that concept model distillation okay in model distillation I need to have two things I need to have

The Admin: P world which is anthropic plot code how does the model predict it how does a particular other model predict a particular token so if the capital of India is I can get anthropics Delhi bai at 025 China.1 banana 03 and runs at 02 and I know what is it that I predict 598 22.13 018 I can calculate something called cross entropy. How different am I compared to what enthropic is predicting and that number is coming as 1.07 and I need to make that number one and that's loss for me. So that is a distillation loss. We are going to look at that later This is my own entropy. This is what I calculate and we can improve this changes but entropy is simple cross entropy for crossover I need to have other distribution. Are we clear on this?

### 01:20:00

The Admin: If somehow you can figure out what is the distribution of anthropic and other models then I can train my model and see my prediction and see their prediction and try and match my prediction to their prediction and I can do distillation. Okay. Chag we are focusing on…

chirag Tagadiya: So yeah. how they come up with what entropics probability is or the estimate. Okay.

The Admin: how is it done how is Quinn actually hacking it how do I answer that in today's session such when you want to steal you cannot say I'm only going to steal your house…

Sachin Bharadwaj: So Rohan for this decision to work the vocabulary has to be same right of the student model and the teacher model.

The Admin: if you're using a non-go lock. You will figure out ways to get the token correct or something's correct, You will try and figure out the tokenizer of coin or opus and try and lose that.

Sachin Bharadwaj: Okay.

The Admin: There are ways to figure that out, All right.

Sachin Bharadwaj: Yeah. Yeah.

The Admin: How do we actually do it mathematically?

The Admin: We calculate our own entropy which is Q into minus log Q that number that came here the R number we calculate that which is 1.06 and then we calculate the us log anthropic Q and I take a sum of that the difference in that is 0.068N 068 Knats is the log number. If there's log x is 4 and log x \- log y is 4 \- 3 1\. So we say ts. So kilometer we use nats for the log number. Right? So that's the difference. And here that formula essentially becomes scale divergence. So the divergence between my model and entropic model is 0.068. So very close. If this number was big then I can start pushing my model.

The Admin: Dude, You need to be predicting this. And then we get something that is very close to stop it. And I'm not kidding. You just need to go to hugging face and then opus distillation spelling is I know. So we have quen 3.535 AB claw opus reasoning. And if I click on it, you're going to see diilled 27B distilled. It's not difficult as much as you think and you do not need the full idea, right? The hack that people use and this answers one of the question is that I will never know that entropic Delhi is 6 and anthropic Mumbai is 0.25 and China is this and that. I will not know that. So what I'll do is I'll start using my model I'll use Opus model to predict something and I'll see the word where it gets diverged immediately.

The Admin: So The capital of India is Delhi. Let's say Quinn answer. So Quen will learn okay no not Delhi. I need to learn new here. So at each point they have a one hot vector to learn from. Not this kind of distribution. There is still closer and that's why it can never match that capacity or that capability but can come very close. We click on this cross entropy. Now how to hack on your network. Yes or all this math not important for This is same thing. here we have what probability did give the right token. Now this is important to understand. Let us say we want a map to be predicted which is a Z0. Now this is a ed 33 zed 4 zed 1 zed 2 zed 33 zed 4\. So there are four numbers.

The Admin: the two ways in which I can get my prediction to be here right let's say a loss of 0.06 06\. There are multiple ways of doing it. Either I increase this or can I reduce this? This is also very important. How do I improve my savings by earning more or spending less? Are we clear on this? That is all this guy is saying. That is why this cross entropy concept is very interesting. If somehow I can figure out we can figure out from other model like OSS 120 the model that Open released.

### 01:25:00

The Admin: Indians can do learn a lot from opus and deepseek and other models which are at least open source instead of just using it and renaming as kutim k1 you can use it and distill your own model at least do that no we'll just recall our own model something but you get the point right if you have something like this you can't figure out some of these details okay are we clear till here okay we have swati once you're done,…

Swati Bansal: Yeah, I'm still trying to get my head around distillation. So, from the whole training process, is it during the data gathering where we capture the examples?

The Admin: once we say we have done training, then you're going to compare yourself to opus and you're going to say we are nowhere close. Then you're going to discuss and we're going to say now we're close.

Swati Bansal: But the cross entropy is a loss function, So, the loss comes into picture during training. No. Yeah.

The Admin: Of course, we have done our training.

The Admin: Say yes I've compared to opus and I'm now feeling sad say yes…

Swati Bansal: Okay. …

The Admin: then I'm going to do this cross entropy distillation training so yes loss is involved for the finetuning and…

Swati Bansal: this is training after we have To further Got it. Okay.

The Admin: making it okay so where does the answer come from this I've explained already so I'm not going to spend time effort but I should spend some time on it So the capital of India is New Delhi The output expected here is capital of India Are we clear? So this becomes my training window.

The Admin: This becomes my output window. will increase this. If this increases, I will increase this. Are we clear on this? What I just drew? Labels are already there. The next word is the label. So mathematically when I'm going to write my for loop, I just have to have two let's say I have a context of 4096\. I have to have two one token ahead and that is my prediction. So very easy mathematically in the moment you write a loop. that's all we have to do in our training loop. Yeah. So we just maintain it. But now this is where the problem comes in.

The Admin: Imagine that I did not have 4096\. let me take a 10 example. It's easier to explain. I did not have 10 tokens. I had eight and then I had to use padding. So I have 1 2 3 4 5 6 7 8 9 pad. 10 pad. I have moved it. So 1 2 3 4 5 6 7 8 pad and then Right now I move my window.

The Admin: So if this is the input coming in this is the output that needs to come in in three tokens out the problem happens here what do we do with the pad because predicting a pad is very easy the network will learn immediately right if you and not kidding I have done it and I got very happy then I learned I felt like my favorite image when I learned why my model was suddenly behaving Einstein time and I realized the kind of stupid mistake I've done. I was feeling like this. Can you see the image? No. No. Because predicting pad is very easy. Let's say you have 4,96 tokens.

The Admin: your data ends at thousand and after that the model has a predict bad because nothing is there to predict bad bad and now suddenly 4,000 tokens are good they're getting exactly the token that I want loss will drop tremendously and I will become happy but when you look at the prediction like inference of the model is going to say bad pat bad pat bad pat bad pat bad pat bad pat bad pat bad pat bad pat bad pat bad pat bad pat bad pat bad pat bad pat bad pat bad pat bad pat bad pat bad pat bad pat bad pat bad pat bad pat bad pat bad pat bad pat bad pat bad pat bad pat bad pat bad pat bad pat bad pat bad pat bad pat bad pat bad pat bad pat bad pat bad pat bad pat bad pat bad pat bad pat bad pat bad pat bad pat bad pat bad pat bad pat bad and you're going to be like what is happening so that is the problem that we're discussing right now and that is where this particular mask

The Admin: comes in. what are we going to do? if we are going to count the pad then the model needs to predict pad and it becomes easy. The loss drops a pad is counted the mean is not going to run over 12 positions and extra ones are trivial. Since the pad follows every pad every time the print loss is going to fall from fall to 0.28 from three three whereas not learning anything. Moment you reduce pad suddenly the loss is going to go up which is the actual loss we want. Are we clear? Here we're shifting by one. And this is another mistake that we do. We take the input and we do not do this one shift for the prediction. And the model predicts the word that it has seen. So the capital of New Delhi output the capital New Delhi and looks at that

### 01:30:00

The Admin: and we feel again happy very small mistake and everyone does it. I've also done it million times, So we have to shift by one first thing and second in padding we are not going to count the pad. We going to mask the pad. So whenever the pad comes in EOS token comes in or pad token comes in that is not going to be part of our learning. Are we clear on Another thing that is there slightly complex to implement but you can especially if you have the EOS token moved in properly. somebody asked this in the last question also. Let us say our token window or the batch size is 4096 tokens. The document we're training on is on chai which is 1024 tokens and the rest of tokens are on cryptography. We would not like to merge the two losses.

The Admin: So we have something called master this target which means that when I'm calculating loss for the initial 1024 tokens I'm not going to take the loss from the back ones just this one it's a separate thread and the second one a separate thread that way I can maintain while doing it but become slightly complex but I still wanted to tell you that there is a way in which you're not able to get the same context document merged together you can use something like this to manage the loss okay and loss and perplexity I've already explained to you loss is loss perplexity is the reverse of it.

The Admin: A loss of zero is propity is one like okay no surprise but a loss of 11 is a huge perplexity and this number looks very similar to our total number of tokens why is that by the way when we start training our model and if this is the total number of tokens that we have our loss is going to start exactly at this number that's why I put this number here what do I mean first of all this is negative log of 131072 and

The Admin: That's the number that you're seeing. Let me negative here to make it similar to what you see on the screen, right? 11.78. So, sorry. Okay. 1 / that's a correct one and then negative. this is how the loss is When our model is randomly initialized and we asking the model to predict anything, what will it ct? Any random token from 13107 to our vocabulary, right? So, the probability of that token prediction is 1 divided by 131072\.

The Admin: you take a negative log of that and that becomes a loss. So when we train our neural network and the loss starts from 11.78 112.1 11.5 we know the model is initialized properly and it's learning and it's going to learn we don't know it's going to learn or not the initialization is correct but if you start a new network and the loss starts from four what does it mean? Anyone Ammon Anisha Swati Sum Balaji Palas,…

Syed Abdul: The initialization had some problem or

The Admin: something is wrong, If your loss does not stop start between 12 and 11, something is

The Admin: wrong do not train okay there some leakage has happened okay for leakage now we have to start training I'm saying that if the loss is not 11.7 moment you start something definitely wrong if it starts at 7 11.7 and within few initial steps it drop to one something is wrong right too good to be true so keep that in mind okay perpix is not comparable across tokens what does it mean tokenizers what does it mean our tokenizer which is

The Admin: good in Hindi has probably one token for a tokenizer which is not good in Hindi probably will have three four tokens for a particular word right so now when it is predicting for example namaste so in that tokenizer let's say tokenizer was bad for Hindi num and were two different tokens so if you calculate a perplexity of after the model has predicted num is going to be very very high right because namaste has always seen together So we might feel that something is wrong. The tokenizer is actually not good in Hindi but the perplexity in Hindi is very low surprise. So the model must be good in Hindi So it's not really comparable like that. So please keep in mind that the two tokenizers are different. You cannot really compare their perplexities. Okay this I have already explained earlier.

The Admin: So if you have 131072 and we have 4K dimensions, we're looking at 500 million parameters that need to be looked at in the input and the output. So it puts a lot of memory pressure on top of us. And if you had a batch of eight, our context is 18K and we are storing our log predicting our logits in BF16 is BR brain float 16 came from deep mind. We have FP32, we have FP16, we have FP8. These are the ITE E designed or defined floating point accuracies or bytes or bits that they use to store a number right but BF float is slightly different when we talk about it I'm going to explain it further invented by deep mind Google if you use that then we have 16 GB gabs of RAM used or memory used and when we do back propagation we always do back propagation on FP32 full accuracy so there we are going to

### 01:35:00

The Admin: is 32\. So 32 \+ 16 we have somewhere around 4 to 4 48 GB of RAM just for one batch. So for eight batches now when we increase it to four and a context increase to 32K you're going to see that this increases and we have a batch of one big context logics and back end becomes even bigger. Right? So we need to keep in mind that the vocabulary puts a lot of pressure on us and that is what you have solved. That paper is not important because you have solved a 1 billion parameter. That paper is important because of this. Now you can increase your context length to a million parameters and it will not hit us like Just this layer by the way. There are other layers which are still going to be hitting us but this layer is not going to hit. Are we clear? Why is that paper so important? I

The Admin: get it right. I need to do more tests. I'm maybe getting happy initially. I need to do more tests to figure out. But initial results are very good. So if that is happening, then our code is going to be running faster. We need lesser RAM to train and pro probably we will be able to beat some benchmark. just to show you bat size eight, context length is 8K and as we increase it, you see that going so takes a whole RAM. Okay. this is important because some of you will be tasked to design your own kernels. What is a kernel? We'll talk about that after we talk about a What is a GPU is a machine that can process a single calculation on lot of numbers together. What is a CPU?

The Admin: A CPU is something that can do lot of different calculations sequentially. So let us say I have to do four and Let's say that operation int is into three on a CPU. This is one step then 6 into 12 fourth step and so A GPU needs to be told that This is another data and this is the operation and this is one step for it. a GPU is if you have heard of this term a massive SIMD which is single instruction multiple data. Are we clear on this? Important part here is data, right?

The Admin: SIMD single operation how big the data is depends on the RAM we have and the bigger the the higher the cost of the GPU Nvidia is a RAM company Nvidia has been selling RAM you take the RAM from Samsung and Hinx put it inside a GPU and sell it doesn't even make GPUs made by Foxcon imagine a company that doesn't manufacture doesn't sell their own GPU they actually sell RAM because that is what is required for multiple operations right

The Admin: same matrix big data when we say context of 1 million parameters or 1 million tokens you need more RAM so I'm going to put a bigger RAM on my GPU that is what Nvidia is going to be doing coming back to what GPUs are really really good at doing the same operation on different data whereas a CPU is going to take multiple steps okay let us say we have a layer we have in the neural network we have some numbers coming in so let's say a matrix comes in and we need to do a simple operation of b And then we are going to do ReLU on top of it. And after that we get let's say we call this matrix C. Okay.

The Admin: You're going to do some reo on top of it. After the reo, it becomes matrix D. the D matrix is going to be multiplied with another matrix called E is going to become F. And then after that we have something called RU and becomes G. Are we clear on it? Okay. The way GPUs actually work is you're going to see this architecture. It has this very very small cache RAM. And then this is fast as possible. If I'm going to show you the speed of this RAM and you're going to say I've never seen anything fast like that. Then we have a Even bigger RAM slightly slower. what I have just done here is I have moved A and B inside calculate C. Then I moved my seat Then for this operation relu I again moved my C from here to here.

The Admin: did a ReLU operation here and then again moved it back here. I D Then for this particular operation I Moved E from one of the storage again to here. Calculated F and again Then for this RLU I again moved my F here and then again did some ReLU there and again moved it back and called it G. We are doing a lot of operations from that HMV which is high bandwidth memory. Right? We're doing something, coming back, and that is a waste of time. What if somehow I can write a kernel that can do all of these operations at once? If I can do something like that, if I can manage within this small RAM that I have there, which is actually in MBS not GBs, if I can manage everything inside that, then I do not need to do this. And that is a kernel. And when you hear a CUDA kernel and all that, that is exactly what people are talking about.

### 01:40:00

The Admin: We ourselves took a lightning model from speed or something like T kernel baseline. Yes, we took our kernel from somewhere around 16,000 or 12,000 tokens per second to something like 50,000 tokens. And this is after some early throughput kernel. But this is again after some optimization. Initially we were somewhere around 4,000 5,000 tokens per second. After we started doing kernel optimizations, we went to something like 49,000 52,000 tokens per second, 10 times the speed up and that is why it's going to be very important and you're going to be writing some kernels. then I'm going to show you flash attention because we are the first guys who essentially took this concept and just made it massively working in that favor. This is the RAM that we talk about when we say the Nvidia GPU 12 GB RAM, right?

The Admin: Then we have GPU HMBB which is 40GB inside that sorry this is the RAM that we talk about when we buy a This is the GPU SAM that I'm talking about. It is only 20 MB. Look at his speed. difference 1.5 terabytes per second versus 19 terabytes per second, right? 1.5 versus 19\. If you want to keep everything in SRAM and all operations must be single shot and that's where the CUDA kernel or the kernel will come in for us. Are we clear? You have some basic idea what a What is a Kernel is something that does multiple operations in one step compared to forcing the GP to do multiple steps in multiple sequences. Right? It's like a truck.

The Admin: You're sending a drug truck gets a toothbrush back to you. You brush your teeth and you keep your toothbrush also. And then toothbrush go package get the toothbrush and toothpaste get packed. It goes and gets packed and come back and then you put it inside a box and then give it to back and say no give it to Amazon Better would be you sit in a truck. If you can't sit in a truck you can do a toothbrush paste in the truck and on the truck you can do packaging and then give it to Amazon. That is actually what is happening in CUDA kernels right and we will do a lot of it because it's so much fun that I can actually show you a small demo or something I'm working on I've turned it off for some time I don't know okay first of all I want to show you I know the camera is small so I don't see you can see here the camera you see this

The Admin: This is a Peltier cooling fan. You can buy it at 900 rupees. which can go up to keep The reason I'm keeping my phone cool is because I'm running something like four or five different neural networks at the same time because I'm doing something like this. I know you can't see I just wrote the stream. One second.

The Admin: Okay, what you're seeing is a OpenGL map because I don't have a camera. I'm going to be putting it on top of a camera. it goes to a neural network that does the real-time depth detection on the phone. Right now, it is processing in something like 35 milliseconds. that goes inside another neural network that does the path planning and that is a drone reconstruction that I have here and I'm training it to hit speeds of 350 km per hour does the full navigation and other stuff identify something figures out a new path and then goes up and down and does something still running but this is way faster compared to my and speed is locked here go

The Admin: I'm showing off, but I'm not showing off because I want to show off or I'm showing off because I'm trying to tell you that this is something I can't do on my Mac also. This is right now running at speeds which are impossible. You see this here 44 and it's taking log stopping. But there are four new networks that are running on the phone at the same time. And if I can give it a cooler which I've done it does that at moninocular depth estimation and that is a metric depth. It knows the depth of that tree that is looking at and then I can one day turn on drone that side essentially and streaming the video also by the way at the same time. that is how important these kernels are. Okay.

### 01:45:00

The Admin: just explain this one thing I want to explain but I'm going to explain it directly in this chunking if we're talking about chunking of the okay so this I explained now fuse the projection in the loss a fuse kernel does the matrix multiply and loss in the one pass writing it

The Admin: only scalar out the few the full log this I explained already process the chunk and the memory and then we cross okay let us say we have to calculate the loss of we have a huge not batch but the vocabulary the sence let's say a sequence length is 16k 16,000 tokens now keeping all of those 16,000 tokens to calculate a loss is a issue because it's going to take a lot of memory. I showed you earlier the graph increases, right?

The Admin: basically this one context length if I'm increasing this you can see that how big it becomes right the alternate we have is a chunk we only do it for 8k at once and then the next 8k other end now that is going to slow my speed down because now I'm dividing it but it allows me to basically reduce the memory required on the app on the GPU so this is the fight that we're going to have once we write our final kernels and the architecture are we going to calculate

The Admin: loss for all the tokens at once and if I do then the context lend is going to be reduced because you want all to be at once or can I chunk my loss calculation also can I calculate loss in first 8K and then and the next 8K and next 8K training as you can seen by now it's not about the architecture at all I don't think we will spend time on architecture but this background is required so much that even if you get the best neural network that exist. You can't train it. Then what's the point of it? That is why there's so much effort on me trying to explain to you that if you do chunking the loss is going to be exactly same. There's no mathematical loss at all. But look at the memory that is required. If I just chunk And of course the speed is going to be slow because I have to do it those many times.

The Admin: So the problem we are going to face is should I run it faster and get a bigger GPU which is expensive or should I run slower and use a smaller GPU which is cheaper right and then I can get multiple of those GPUs also to get back to some speed. So here are dynamics of things that we need to manage that is it possible for me to get the biggest possible GPU and train on it. then we will do that. But if you figure out no, there are some optimizations we can do that allows us to use a smaller GPU and get to a similar speed, we will do that, right? So that's a cost advantage that we have to calculate because it doesn't make sense to go with a $1,000 per hour GPU and just exhaust everything. Then we have not trained. We need to figure that out and that's a important task that we have. Okay, another thing.

The Admin: As I said we multiply things and we do stuff and I showed you in the cross and droppy calculation also. which is softmax calculator we go here and then let's say I not don't do three I do 30 and calculate this you're going to see it is actually normalizing it. I don't want no values. because this is a calculator, it is capping it to one. But what happens sometimes is if you do not cap it, for example, we have a logit of 10, the value comes to 9.6. If you have a loit of 60, the value comes to 28.9.

The Admin: If you have logit of 600, we sort of seal it. What I'm trying to tell you here is if you do not how to explain okay we're only focusing on logs. So we discussed that logics can be 0 1 \-6 \-16 \-600 6,000 and so on. Are we clear on this?

### 01:50:00

The Admin: Yes or If we do this unbounded logic calculation, sometimes while calculating this some values go so high and so low then we get ns in our training losses. What you need to realize is when you do something on calculator or online that we did we have a fixed equation there and there so write a function to divide two numbers get a and b and return by b. Is this clear? Simple Python function. Yes or no? Can this function fail?

Syed Abdul: Yes.

The Admin: Yeah. So you add a condition that B is not equal to Z then can the function fail. Yes or no?

The Admin: Yeah, we can send B as a binary or some other alphabet. There are so many conditions that you need to add inside just to make sure this doesn't fail. So when you see online demo on a calculator or other stuff and you go and calc cross and drop and the value comes in, don't assume that There a lot of things that go inside to make it stable. Similarly, when we calculate a loss, all the logic values cannot be calculated. There are some u conditions added because of FV16 cannot make that number and some things do you know that a computer cannot write 0.1 \+ 0.1 equal to 0.2

The Admin: too. are you aware of that? Mathematically, it's not possible on any computer invented ever to be able to do this because you cannot represent some numbers at all because of the way we represent binary and all because of which and if you keep it unb unbounded we get into an issue of getting ns and our loss function just crashes. So we add a cap is called soft cap. So a soft cap of 30 which means that this is going to be negative 30 this is going to be positive 30\. We do not let a number go beyond a particular number. That's called a soft cap. And in our case, we had a soft cap of 15 when we were training and that gave us a lot of stability. That is what being discussed here. So logic soft capping is something that we are also going to implement. And these are things that we have to do to make sure the law sustainable and they are being handled properly, And this is how it's going to look like. You have two runs here. You have this one and this one.

The Admin: And you're going to see in the loss side all of them might actually look good on the ne network but you can see how fast one trains and how slow are the trains. the purple one the soft cap of 30 you can see how fast it is actually coming down compared to other numbers right new network eventually will come together but we want to be in this state compared to the blue one state. Clear on this you understand these graphs there are 1 2 3 four behind three behind each other. the red and the green are behind each other. Whereas the teal one is coming down faster. So we have to find this also for our new network. When we are training we have to figure out what is the soft cap we going to be using and so much to do that is why we have so many students and if you remain active by now we training it then some of you will have to figure this out and actually help.

The Admin: When you ask or think about what is it that I'm going to do in neural networks or training Ron is going to share the code he's going to share the tokenizer he's going to train it what will you do this is what I had to do earlier all these experiments you have to do there are a lot of things that we have to figure out you're going to run it properly and you're going to come back and Okay, according to my experiments, the soft cap for us should be this value. According to our experiments, this is the right architecture. According to our experiment, this is what we need to do or tokenizer should be like this and that, So many floating elements that you have to contribute. this is another idea that we may not be using. it's just worth knowing just what we did in the memory side calculating loss for first thousand tokens then second,000 tokens and third,000 tokens.

The Admin: we can do something called adaptive softmax. I went very close to implementing it. It is already implemented using it. but then dropped it because the accuracy is not as close but I think in some scenarios it's going to be super useful to you. what this says is I have a vocabulary of how many 131072 tokens right and I have to calculate softmax of all of them. But wait, I'm only talking Telugu. My whole text is Telugu. Why should I be even calculating loss on English and other maths and coding and other stuff? I can probably Not drop it but use it if I require if you think like that what you can come up with adaptive soft max where based on the frequency you can calculate the loss directly immediately fast because you have not found a word that is not in that small cluster all those tu words are already there but if you do get six if you're not careful of keeping six with you or if you do get Einstein written in English then you have to break that chain and sometimes go in the rare cluster and calculate loss from there.

### 01:55:00

The Admin: So what you're going to see here is if you hit this cluster the amount of time you're going to take is anyways what you have to take you have calculate the whole softmax but fortunately those words are not there then most of the times you're going to be actually here so amount of RAM required and the speed that we get from doing rap to softmax is good but I didn't get enough time to be able to implement this last time properly and this is another area by the way where you can also think of to come up with some sort of adaptive soft form which is better than adaptive softmax can allow us to go closer. The reason this is not as good as normal softax is because even though you're predicting a Telugu word, you still want to know that I'm not going to predict Einstein and I'm not going to predict something written in Chinese. So you still have to say not Saying no is more difficult. So that is why it is not as good as adaptive as the normal softmax. this is one thing that we really did and we found improvement also. This called multi head prediction.

The Admin: Multiate prediction is that we don We actually predict many token So right now we do something like this. We have our head one which is taking one ken inside from the last step. Right? we are taking one token in and we're predicting the next token out. Are we clear on this that we have always discussed this? We have never discussed MTP which is multi head to here is multi head token prediction. What it does is it has head one which predicts token number T1.

The Admin: Then it has head two which simultaneously predicts a token number two. Then we have head three which predicts a token number three. And here we have token number four. You can go up to 8 9\. how does it help? first of all let's say this layer was 1 billion parameter. We We have to have One billion here also. So we add three billion parameters. But I'm predicting four tokens at once. Right now training this is complex but if you train it then the wins are really really amazing. Okay. And how do we actually train it? Okay.

The Admin: So token number one 2 3 4 5 6 came in. So here what I'm predicting please fast. Okay 1 2 3 4 5 6 came in.

The Admin: What token number are you predicting?

Umesh Nmenon: And eight.

The Admin: Seven. Right. And in case of NTP, we are also going to predict eight. Yes or no? we have two things in training and in training is easy. I know the token number seven and token number eight. I can immediately figure out loss for token number eight. I don't have to do anything fancy here. Are we clear on this? In training, I will always be predicting token number six, getting seven and getting 8, 9, 10, whatever is there and I can immediately calculate my loss. But the next token that goes inside is seven only. We always train one token at once in case of training. Are we 100% clear on what I just said? Chundraas, you're not speaking today. Got to Okay, This is the training part. During inference, magic happens. And I want to focus on the inference part because that is where the speed up comes in.

The Admin: We have token number one two going in and model predictor three four five and let's say six also okay I know this is all okay the token number three will always have the higher performance or better performance compared to this and this because they are speculative they may be there so I'm going to feed in all of them three four five and six okay now three I know was correct because that's Next token I'm predicting it's correct or not. We really don't know. We are talking about inferencing but it's a really good model. So we know the next token is definitely good. Are we clear on this?

The Admin: Okay, I need to draw it again. So, one, two goes in, three comes out, right? And four comes out, and five comes out, and six comes out. Now, I'm going to be feeding token number four, and token number five, and token number six all together for the next prediction. Now, we know that this is So token number three came in, token number went Four is also going to be accurate, I know that. Now I'm going to compare that the token I'm predicting now is same as the token that was predicting last time. if it was last time, whatever token I predicted, I'm just going to carry forward that right. Then if these are same and the token number five that was predicted was the prediction that I'm predicting right now.

### 02:00:00

The Admin: And if this was matching this one, six will also go through. So while inferencing we do a immediate check, Let me explain this So capital of India is new and Delhi. We predicted two tokens simultaneously new and Delhi. Right now in case of a to normal model I would predict this is the input and this is the output I will get. But in case of MTP multi token prediction Delhi would also go. So when next time I fit in a model capital of India is new and Delhi will directly go in. But how do I show you Third one also I have to show you one more example. Okay.

The Admin: the capital of correct we can use that here Dallas is in United States of America right so we have 1 2 3 four four tokens that are going in the model so Dallas goes inside these four tokens come out. Now I'm going to feed these four tokens as is United States of America. The cost right now is one forward not 1 2 3 4 forward. That's what I'm trying to tell I'm feeding four ones at once to the model. And if the model happens to predict United States of America, I have won the speed up. Instead of running four times, I had to run one times.

The Admin: But if this was wrong and only if the states was wrong then I have to again do this part. I have to run them one by one. Right? So speed up comes in how many times my speculation was correct. You clear on it? The same thing which is trying to show you. Now loss is going to be the loss of the fourth token that is not important but depending on how many words you're predicting a model will behave slightly better. So somewhere around MTB equal to three people have found that the loss is actually slightly better but we'll do that calculation also again say

Syed Abdul: Yeah. So my question is so during training does for example when the input is delas is in for the second we explicitly train for states instead of

The Admin: We do not feed four. In training we always predict the next word. We always get to know the correct word. So in training in training we would have done Dallas is in United States of America. Right. So Dallas is in Okay.

Syed Abdul: Yeah. My question is the head two would not even get the input united will directly

The Admin: This will go the modelic United States of America. This is my loss. This is my L3 loss and my L4 loss. I will calculate all of that and back propagate. One second. This is how my loss will go in. Next time I'm going to do Dallas is in United and states only. And the model is going to predict America full stop. And I'm going to calculate loss L3 and whatever L4 was. So the feed to the model is always one word at one in training. We do not leverage the inferencing speed up that we get while training.

The Admin: While training is always one word and I calculate a loss for all the MTPs and back. Now ask your question.

Syed Abdul: Yeah. Yeah.

Syed Abdul: While training we do one at a time. But my question is when doing the loss calculation we say that the ground truth in that image itself in your blackboard for L1 the ground through token is every…

The Admin: H. Yeah.

### 02:05:00

Syed Abdul: but for L2 the ground token is token not every.

The Admin: Correct. Yes.

Syed Abdul: So for L2 it thinks that the input was the model reads output should have been token.

The Admin: Correct. Exactly.

Syed Abdul: So the L2 head is being trained that for whatever input I have to predict one plus token irrespective of one token.

The Admin: Exactly.

Syed Abdul: So I have to keep those four heads always extra. Okay.

The Admin: And there are a lot of news and again these are speculations that are not proven or written in paper. Sometimes they are written.

The Admin: There are a lot of times where people train up to MTP4 that helps in the loss calculation but because it is sort of showing you where the model is trying to predict right so you want to adjust it early on so it helps there but while inferencing or while deployment they only use MTP1 because the performance drops after MTP 2 and three very interesting So you train till 4 head you think in advance what you're about to say but you don't actually deploy it because the performance of deployed model is not as good. So you may train at four heads but you may only deploy two heads. draft and diversity. basically as you're training it you can change the length basically right. So how many of them we are keeping how many have been dropping.

The Admin: So what it's trying to say is if you were accurate four out of four then you have to throw away nothing. All four heads were correct but if the last one was wrong then you're correct three or four. If the first one is wrong then you have to throw everything that is coming in front. That is all what it's trying to show. And you can see that acceptance rate depending on how good your model is you can 2x the speed of what you're predicting. So it's really really good. here the topics are essentially that are for the sessions that are about to come. So we're not going to touch them. But these things we are still going to be touching. for example we have fill in the middle not used anymore. We only predict U for example We predict the next token and that becomes a loss. Fill in the middle basically means that Dallas pays United States. So what is that? We have to predict in.

The Admin: So not used but one of the way you can calculate then we have something called Label smoothing essentially is that we do not force our model to predict one as a one hot vector. We ask our model to predict more like 0.9 is good enough. So one hot vector for us is not always going to be one. You clear on it? We will not force the model to predict one 98.96 and that is How much smoothing you want? That also helps. Then we have something called load balancing. MO is mixture of experts. When let's say we have never discussed experts but our model is going to be when we have experts inside. Okay. So what are experts?

The Admin: We saw one attention one transformer layer, Imagine that instead of one layer, sorry, you saw one FFN on top, instead of one big FFN, why don't we divide that FFN into multiple small FFNs? And each FFN is called an expert. So M OE architecture basically So instead of one FFN, we have four here. Can have 400\. We can have 4,000. And just to give you an idea, let's go to Greek seek the fourth M O

The Admin: E activated it's look at the How many activated weights are there? What is model size? Everyone can see that number 1.6 trillion.

Soma Korada: Stop.

Avnish Midha: Yeah. 1.6

The Admin: These are the Total weights that are there. How many are Activated basically means used for predicting one token 49 billion look at the ratio of that right and this is an amazing ratio we're saying 49 billion of one six I don't know how many four so around 3% only 3% of the weights actually take part in predicting a particular token these 3% are not same by the way they are random sometimes those 3% so why do we call them experts because they notice that

### 02:10:00

The Admin: for a particular topic or context a particular kind of expert fires. So that expert focuses on science for example the other focuses on cricket the other expert focuses on political science and politics and other stuff and finances and banking and drawing and being creative and being scientist and being rude and being happy So MO load balancing basically means that if you're only talking sad things you do not want the happy expert to die. So somehow we keep a balance. Somehow we have to add a loss for these experts on top of overall loss that we have to make sure that our load balancing doesn't crash. Some experts are always there and that's a difficult thing to do. Deepsec has done really good work on it. So we'll talk about that also. Then we have the Router Z. So MO load balancing basically means all of the experts should basically behave in the same Another way of looking at it is to add a router loss which decides which expert should fire.

The Admin: So we have that loss also. So all these are going to come in the future sessions. Then we have supervised the same loss but it's masked. We have already discussed this. Here we are masking the prompt. So we are not calculating loss on the prompt. We can decide to train on the prompt also. Wrong strategy for post training. So when we do post training what is the capital of India? We do not ca We calculate loss on the capital of India is New Delhi. But if you were to add it then it's a wrong training. That is not how we do it in post training. We're not going to calculate the loss on what the capital of India. Then when we are going to be in the RL stage which is probably six seven sessions away from today. there we're going to be talking about the reward laws. How do we tell the

The Admin: not only a good or bad and here we are going to be using something called Bradley Terry loss very simple loss but the guy invented his name was Bradley Terry loss that's why it looks like a terrible loss name to remember but very very simple loss what it says is what is the capital of India New Delhi one answer what is the the capital of India is New Delhi two answers which answer would you prefer now that's where the preference will come in so we're going to ask humans to rate but for all the questions we can't ask humans to

The Admin: So we're going to ask it humans to rate at least 100,000 of them. So now we're going to train a model which learn Then we're going to use this train model on humans to rate the neural network on how humans would have rated. Now we can scale this All we're doing is basically you're laughing. No. This is what Open AI did with Open AIA training. Not This is how and people use other people and think of this. Kenya is involved in open AI and training and charges. calm Everyone remembers occur. But that is what is happening here. We are essentially asking humans to create something. Then we use that to train a model and the model just says one and zero. And we use that to now train the model. Right?

The Admin: And we're going to go in more detail about this but I just want to give you an idea of how this can be done. Now only the gap basically we need to do both basically. We need to reduce the loss of the loser and we need to increase the loss of the winner both at the same time. Right? That doesn't matter. We're just more interested in loss. Basically the u answer that you didn't like and answer that you liked we have to punish for both of them. That is what all this graph is trying to say. This will get very clear when we are in the RL model. here are topics that are even more complex. So I'm just going to brush through them what they are. There's something called RLHF reinforcement learning with human feedback. I already explained that those humans were keen.

The Admin: So if you have a keen human sitting in the neural network chain somewhere telling the neural network to learn and then that new network trains the other neural network in preference that is called RLHF. Now a lot of humans are required not scalable you could not ask all the question that you wanted to ask and old model was trained on its own data new model how do we train on old model data and so on complex. So people came up with PO then we came up with DPO then we came up with KPO then DPO these are not the right terms sorry we have DPO we have GPRO and we have all the other things these are advanced terms that we need to discuss when in session 14 I've kept them here so you can come back to them and learn about them when the time is right of course we are going to cover them it's not just the reading material so PPU

### 02:15:00

The Admin: Then All of them have different logics. DPO came first. Here we need a policy the model that we're training. Then we had to have a reference shown as a small model here. But a good model that I'm trying to copy or I'm trying the master model basically. Then we have a reward model that thinks human and then give the reward. Then I have the Then model that I train. Then we have DPO where I do not need reward model or volume model. I just need to have a reference and I can directly train my policy. Then I have GPRO where I can have a reward model and a reference and so basically all of them here what is most important for us money by which one is going to cost us less and gives us more. Now after I wrote this session for you, I came across this paper. I can't even show that paper to you. Do I show that to you? I have opened it somewhere.

The Admin: Yes, this is a magical paper and I can't tell you how happy I am after looking at this paper. came very recently and can you read the name of the paper embarrassingly cheap post training and I saw that and I said dude all this is what I need right how do we do embarrassingly cheap post training and I can't tell you how good this is I know you will not read the paper it's Saturday anyways and who was going to read all this so I'm just going to show you the results this is the result the RL model and the kura

The Admin: their model that is red one and red one is beating the base model and the RL model after spending should show you how much money they saved because kita is the only question that humans Indians ask when we buy a car right so if you use reason maxer you'll spend $4 compared to $1200 for computation for co 2.51b just look at this one $103,000 compared to $25 for reason maxer and it's damn simple What we do is we ask a question to a neural network to the LM for which we know the answer. there's this thing called I explain temperature multiple times to you. We change the temperature and we ask a new network again.

The Admin: If the answer changes and if it for some temperature gives me the correct number that I remember that example and I remember the temperature settings and everything. I ask another question and I change the temperature and the answer doesn't change. It will always give me the wrong answer. those I'm not interested in. I only train on this thing again. I'm training the neural network on things on which the model was confused. The model didn't know. For example, Akbar's fourth's son's wife's name was what? Model doesn't know.

The Admin: it's never going to answer it. But if you ask a complex question and based on some temperature setting actually gives the correct answer or correct answer or near answer, they just collect that data set. So you have a model, you change the temperature on multiple questions, you look at the response and you only save those responses where the answer could have been received. You only take them and only train on that. That's it right only punish for that. And there's a beautiful work that they've done and really brilliant. So if you do get time I'm going to share this link with you guys so you can also read So which model I don't know we going to use GPRO DPO BPO KPO but all of them are there and we can figure out which model we can use but this is for future as I said. Now distillation I also explained the loss map there many things that we need to be aware of. This is how the session looks like.

The Admin: We will have perlexities at loss, memory, safety, robot model, PPO, DP, GPR, RBI, IPO, KP. So the new distillation. Okay. So what do we have to decide? We have to decide a few things. Are we going to be using a factor We're going to be using MTP and how many of them? Are we going to be using a chunk size? What is going to be the head stability for us, which is the Z loss, soft cap and centering? Are we going to do all of that? we don't have answers for them, For each model, the behavior is different. We going to write a model the whole LM. Then we are going to perform some oblation studies and we're going to get some test data and from there we're going to understand that this can be done or not. This is exactly where the Chinchilla law saying that says that you can take small model train on it get all this fixed and then train a bigger model. That's the actual use case and we're going to be using it for that. So what is assignment? Finally I get to stop speaking and you get to listen and you get to work.

The Admin: I have to work for a week to give you some work and you go to cloud code and finish your work in a day or two. This is also a small one only but I didn't give you a complex assignment this time because I really want you to go through the whole step at least once. Look at how the training is done on a small thing. try to look at the code. It's not difficult. It is written in English. I know you can read English. There are few alien terms Don't get scared. It is importing a module only. Then there's something called a layer or Do not get afraid. they will not bite you. just try and read that simple line of code. So what you have to do is write a small harness define a model and you can use Garpati's GPD2 or nano transformer or any architecture that you want. Look at how the model is print every tensor shape that is there.

### 02:20:00

The Admin: the size. How do you know a particular dimension for a particular token or a layer or attention there? Try and dig inside it. Talk to cloud code. No problem. But ask it to write code and then show the result to you. Don't ask what is the dimension of layer number seven. Write the code in the terminal and execute it and At least do that. Look at the code. Then verify the shift. For example, print the actual token string input inside the target not the ids actual strings. Then do the mask padding what we discussed and then train on it and Then back two documents in one sentence and try and mask the boundary. Then compute perplexity. Ask it to show you the code. What does it look like? We do not want to be generation. Who doesn't know how the code looks like? I read it yesterday.

The Admin: code is becoming write only and disposable. These two things I never thought I would hear about So code today is write only and dis very interesting. Then compare the tide head against the untied head only a small model literally a 20 million parameter model on some let's say fine web 10 million or 20 million tokens or if you don't want to do that use Shakespeare not a problem. Then add the part two is add one extra head. What are you submitting this time? Okay, either I'm going to change this again. Either you're training it on your own computer. If you have a Mac, request you to train on your Mac because it will have a better RAM. If you don't have anything and you're really poor, you don't have money to eat and food to drink and car to wear. Then you can train on something called Google Collab. It gives you 8 GB or 12 GB of RAM or four five hours. You can train on top of it and submit the numbers. I can stop speaking. You're submitting a GitHub readme link.

The Admin: So I can go there and you have done work. I need to see your file also. So I know that we've did work. All right, Session has ended. You can go now. If you don't have any questions, no questions. Yeah, I need to map it and…

Syed Abdul: Not a question but you could share that annotation tool Okay.

The Admin: share it and upload it somewhere. and it's my copy. So, I need to just test that part. Okay. L line by line will go.

Anirudh narla: Sir, the link at the start about

The Admin: So happy we get the one hot widget at least.

Soma Korada: Rohan, I'm still confused on the distillation part. how do we get logits of the model we are trying to compare against? So one hot log I mean we know what is the word which needs to be predicted for that we don't need any reference model right.

The Admin: How do you know what word opus is going to predict for a particular quoting task that you have given?

The Admin: Tell me what is the 400 word opus will say if I ask it to work on my repo some No,…

Syed Abdul: Give lock props in their API for their final layer.

Syed Abdul: They give the lock probabilities of their vocabulary and timing. CL does not give but open eye

Soma Korada: So we can do distillation only for the models where we have this available.

The Admin: as I said, one hot is good enough.

Soma Korada: one hot.

Soma Korada: Okay. Yeah.

The Admin: You have something and I'm asking a question. You're not answering it again. M open air or…

Soma Korada: Yeah. got it. Okay.

The Admin: a cloud is going to predict if I share my report. Do you know that? so we need to know how plot things for every single token. At least get that and that is good enough to train. We know it's not the desired ideal distillation process but that's the best we can do. That's why the gap

Sandeep Kunkunuru: Can you throw some light on unified memory and how that changes anything that we are doing right now?

The Admin: what do you mean unified memory?

### 02:25:00

Sandeep Kunkunuru: What I understand or…

The Admin: can tell you no not true for all operating systems only true for Mac on Mac and…

Sandeep Kunkunuru: what I picked up is that GPU and CPUs both share common memory and there are no memory hops between CPU and GPU and that could be helpful in some workloads.

The Admin: this is only true for SOC so all mobile phones Mac and everyone else for all tablets but not Windows no not Intel okay what SOC is system on chip is that we have a chip and in that chip

The Admin: The CPU stays here and GPU is here and everything else is here and the RAM essentially sits on top of it. So this was a 3D model. The RAM is going to be something like I'm going to show you RAM is going to be slightly taller also. And then inside that you will have this kind of slot. And this sits on top of it. So it covers it. That is the unified memory. So CPUs and GPU share the same True for Mac, true for all phones. But for Windows or Nvidia graphic card, you have CPU where you have a separate RAM and then you have GPU where you have separate RAM. And here we have to travel. Here we don't. All right.

The Admin: What else?

Anirudh narla: Would you mind sharing the draft of the paper which I think you presented at the start the paper which you guys were working on.

The Admin: The answer is no. and if you share it outside then we cannot write the paper. So it has to be written first and then shared.

Anirudh narla: Okay. That's fine.

The Admin: One second.

Dattatreya Manjunath: So I'm just trying to understand you mentioned that if distillation has to happen the tokens have to be same or we'll have to figure out how the tokens are I mean what exactly the tokens match right I'm just trying to understand right if we know the Third.

The Admin: One second. So I Just open this link coin 3.6

The Admin: six model open distillation I'm going to go to the files and I'm seeing the safe tensors are there right this is the model that is already trained now I'm going to hugging trace purpose this t data set now if I go at claw disters in fact I can go to fable also because I remember seeing fable okay this is some guy helioai fable 5 distillation

The Admin: reasoning what they have done they've added a query and they got the thinking so now you have the thinking trace of fable you can use this to force a model to exactly emit the same token I know this is not telling that this second token should have been that but this is really really good compared to what otherwise is there then let's look at other fable also the favor SFT here we have one example start of the session you get a helpful Agent I am end user make a new one. It should be a fast and blah blah blah and then we have other commands coming in. Okay, this is what the model is thinking. The user wants me to create a modern data blah blah blah blah blah. So we just make our model forced to predict this. So do I have the perplexity or do I have the softmax values or logic values and all the other characters at the first location? Answer is no.

The Admin: That's why I said that for these models which do not share the prop max or probability per token we just and make that as the only token that should be predicted. So we get a model that is very close to favorable…

The Admin: but not favorable because we can't replicate the overall behavior for every token. Now you can ask a question.

Dattatreya Manjunath: Got it.

Dattatreya Manjunath: Yeah, that was the question because I mean that removes the dependency on even understand knowing exact tokens, We just want to figure out the word and…

Dattatreya Manjunath: it can be multiple tokens. That's kind of what my question is.

The Admin: Okay, which experience?

Aman Gupta: Rohal, are you using any open source data for the experiment you're doing with the knocker tokenizer.

The Admin: I didn't get the question.

Aman Gupta: The question so I'm asking are you using for all the experiments…

Aman Gupta: which you are doing with the knocker are you using any open source data or it's internal data which you have?

The Admin: What?

The Admin: Everything is open source.

The Admin: What do you mean?

Aman Gupta: Yeah. I mean …

Aman Gupta: if I want to replicate the experiments which you are doing and want to compare.

The Admin: I have to publish it.

Aman Gupta: Yeah. okay.

The Admin: Only after publishing it becomes open source.

Aman Gupta: So you're using the internal data which Okay.

The Admin: Yes. Yes. Yeah.

Anirudh narla: Hello sir. Yeah, regarding distillation. Yeah sure.

The Admin: That's correct.

Anirudh narla: This approach of you just training it upon the teacher model that is also good but if you let's say had access to logic probabilities and all that then it would be even more accurate right Okay.

### 02:30:00

Dattatreya Manjunath: This question is more about last class so basically we have a 4096 let's say vector right and then we basically divided into four different heads each of 1024 right and then attention is calculated on that 1024 and we basically assume that back propagation takes care of making sure each head in itself has all that information.

Dattatreya Manjunath: So does that necessarily mean that our 4096 is converted to some latent space of 102 so 4096 is converted to 1024 latent space and each 1024 has some fraction of all those dimensions and we can I mean because it's just a fraction of 4096 is there a degradation of attention mechanism that happens is there any paper that works

The Admin: We have 4096\. We physically split the memory into four blocks and each head work on these blocks. head three, head four. After the attention and everything is done, we concatenate it back. So we have 1, two, three. And that is why another answer why FFN is needed. FFN now looks at it and now looks and expands it to 4x and then compresses it back to 496\. So it is a task of FN to figure out okay this guy is saying maintaining the animal and all the other instincts but the guy looks like more on the cricket so I need to make it zero so we do not lose anything.

Dattatreya Manjunath: But there's also attention between words. that's what is propagated here, That's what I was trying to right.

The Admin: So attention between words is happening 1 2 3 4 another words first head is going to talk it to this head. So they are only talking to themselves. The Head mixture happen in FFN.

Dattatreya Manjunath: So my question was more along let's say you have Dhoni whose major identity is associated to cricket and then you have let's say some other Dhoni not behind the scene right and there's a fraction of it is cricket right and both of them is provided and it's just a fraction of that association is computed here right in each and every head does that automatically learn when back propagation happens. I'm not sure if I'm putting my point across correctly.

The Admin: Sorry. I was on mute. so just think about your question again and ask again. Swati not is the top.

Swati Bansal: The multi-token prediction which you're talking about how is that related with top okay that you mentioned last session

The Admin: Top case is per token, not across tokens.

Dattatreya Manjunath: Hello.

The Admin: Yeah, please ask.

Dattatreya Manjunath: Yes, sorry suddenly the audio froze. I had to re rejoin. if he was answering something about the question I had previously asked, I could not hear that.

The Admin: No, you answer yourself. the back progressions figures out automatically because the loss has Yes.

Dattatreya Manjunath: It does. Okay. Pix.

The Admin: All If no other question then I'll see you on next in the meantime I'm stopping the recording.

### Meeting ended after 02:34:49 👋

*This editable transcript was computer generated and might contain errors. People can also change the text after it was created.*

