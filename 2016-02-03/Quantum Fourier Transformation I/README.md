# Quantum Fourier Transformation I

So, you want to learn about *Quantum Fourier Transformation* (QFT), but have no idea about either *Quantum Computer Science* (QCS) nor so called *Qbits*? Well, that's the reason I'm writing this posts: to explain to you what QFT is about!

But let me warn you: It took me about a year to get my heads around even the basics of QCS, and I won't tell you in the following posts – I'm hoping to produce in the coming weeks and month – each and every single detail! However, I'll try to provide enough context information so you get the big picture and can go digging yourself for more *entanglement* with reality! Alright, let's throw you into the cold water! This is the QFT:

![QFT: Quantum Fourier Transformation][1]

Well, it's a circuit diagram of a QFT with four *input* and *output* Qbits. Just wait a minute: "What is a Qbit?" I hear you screaming. I did not explain it yet, did I? And "what are these funny brackets around $|x_i⟩$ and $|y_i⟩$?" And "what is $\textbf{H}$?" Further, "why do you have these numbers in these circles, what do they do?".

Just slow down, and let me explain: A lonely *Qbit* is a magical box, since sometimes it's zero and sometimes one! Often, you have no idea what it will tell you, but sometimes you can gleam an answer by judging its mood. It's an entirely different beast compared to the classical bit or *Cbit*, but if you treat it nicely, it will provide you with the answers you have been looking for..

A *Qbit* is like the oracle of *Delphi*: offer the correct kind of gifts, and ask whatever your heart desires. If you time your question precisely, you will be rewarded with a revelation. But be careful: Often the oracle provides you with the correct answers, but sometimes it's just produces junk! So you need to learn to distinguish the truth from the not so true statements.

Another problem with the answers might be, that you may have asked the wrong question: Well, I'd advise you to maybe repeat it to clarify matters, since otherwise, if you set out to destroy an empire you may very possibly doomed yourself!

Alright, after this rather confusing analogies let's get precise: A Qbit is essentially a vector: A zero $|0⟩$ *ket* is a column vector equal to $\begin{bmatrix}1,0\end{bmatrix}^T$, and a zero $⟨0|$ *bra* the corresponding row vector $\begin{bmatrix}1;0\end{bmatrix}$. Further, a one $|1⟩$ ket is the column vector $\begin{bmatrix}0,1\end{bmatrix}^T$, while a one $⟨1|$ bra is the row vector $\begin{bmatrix}0;1\end{bmatrix}$. It's simple! To be more precise, a $|0⟩$ or $|1⟩$ are the pure states a Qbit can be associated with, whereas the general Qbit looks like:

$$\begin{equation}
|ψ⟩=α|0⟩+β|1⟩=\begin{bmatrix}α\\β\end{bmatrix}
\end{equation}$$

where $α$ and $β$ are complex numbers. So, I've told you that the Qbit $|ψ⟩$ sometimes likes to be a $|0⟩$ and sometimes a $|1⟩$: There is not much you can do, it just does what ever it wants to do! But it's not completely (uniformly) random – no, there is a pattern! Namely depending on the probabilities $|α^2|$ and $|β^2|$ with:

$$|α^2|+|β^2|=1$$

it will tell you either $|0⟩$ or $|1⟩$. So, if we can adjust these probabilities we can control and influence the Qbit to run useful calculations. So, the subject of a Qbit should be crystal clear by now. Let's investigate $\textbf{H}$, which is a so called *Hadamard operator*: I like to call it a washing machine, where you throw in a $|0⟩$ and a $|1⟩$ and you get the perfect mix! The result is neither a $|0⟩$ nor a $|1⟩$, but somehow both.

So, in crisp mathematical language an $\textbf{H}$ is a matrix (operator) that when multiplied with a column vector produces another column vector, namely:

$$\begin{equation}
\textbf{H}|0⟩=\frac{1}{\sqrt2}×(|0⟩+|1⟩)=\frac{1}{\sqrt2}×\begin{bmatrix}1\\1\end{bmatrix}
\end{equation}$$

and

$$\begin{equation}
\textbf{H}|1⟩=\frac{1}{\sqrt2}×(|0⟩-|1⟩)=\frac{1}{\sqrt2}×\begin{bmatrix}+1\\-1\end{bmatrix}
\end{equation}$$

Therefore:

$$\begin{equation}
\textbf{H}=\frac{1}{\sqrt2}×\begin{bmatrix}1&amp;+1\\1&amp;-1\end{bmatrix}
\end{equation}$$

So far we've not encountered anything complicated: Just a bunch of definitions combined with some probabilities to model the inherent uncertainty within the realm of the quantum world.

Now the next question: what was it again? Yes, "in the QFT circuit: what are these funny dots with the numbers?" Well, the answer will be revealed in my next post!

Till then do some multiplications with $\textbf{H}$ and figure out its properties; alright? For example, did you know that $\textbf{H}$ is unitary – figure out what that means and prove it! Further, $\textbf{H}$ is also its own inverse, i.e. $\textbf{H}^2=1$, where the latter is the unity matrix: again prove it, will you?

[1]: https://2.bp.blogspot.com/-nj954YSSNqU/VtGIro8VoSI/AAAAAAAAAR0/yQ9Tgn7CcjM/s640/QFT.png
