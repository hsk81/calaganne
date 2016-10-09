# Quantum Fourier Transformation II

Alright, let's have a deeper look at the *Quantum Fourier Transformation* (QFT):

![QFT Circuit with four Qbits][1]

As you see the particular QFT depicted has four *input* and four *output* Qbits, where the boxes with an $\textbf{H}$ inside are *Hadamard gates* and where the circles are 2-Qbit unitary operators. How do we formalize a QFT? Here you go:

$$\begin{equation}\textbf{U}_{FT}{|x⟩}_n=\frac{1}{\sqrt{2^n}}\times\sum_{y=0}^{2^n-1} e^{2{\pi}ixy/2^n}{|y⟩}_n\end{equation}$$

Essentially, it looks like a bunch of roots of unity summed over $y$. There is further another very beautiful expression of $\textbf{U}_{FT}$, which is based on the $\textbf{H}^{⊗n}$ and $\mathcal{Z}^x$ operators:

$$\begin{equation}\textbf{U}_{FT}{|x⟩}_n={\mathcal{Z}^x}{\textbf{H}^{⊗n}}\end{equation}$$

where $\mathcal{Z}{|y⟩}_n=\exp(2{\pi}iy/2^n)$ and $\textbf{H}^{⊗n} = \sum_{y=0}^{2^n-1}{|y⟩}_n$. Further, the 2-Qbit unitary operators $\textbf{V}_{ij}$ looks like:

$$\begin{equation}
\textbf{V}_{ij}=e^{{\pi}i\textbf{n}_i\textbf{n}_j/2^{|i-j|}}
\end{equation}$$

where $|i−j|=k$ corresponds to the integer you see in the circles above and $\textbf{n}$ is the number operator $\bigl[\begin{smallmatrix}0&amp;0 \\ 0&amp;1\end{smallmatrix}\bigr]$. Notice how the wires end up upside down, which is another particularity of the $\textbf{U}_{FT}$ transformation. It's actually quite a bit abstract and difficult to imagine why and how QFT could be useful, but if you remember your regular *Fourier* transformation, then you will recall that an FT is essentially a mapping to the *frequency basis*, allowing us to figure out immediately certain *periods* of a given function.

This is exactly what a QFT delivers too! Just the quantum way, i.e. we will *not* be able to see all frequencies at once, but we'll be able to query for the most significant ones (if they have a high probability). So, the trick is to prepare our *input* and *output* registers such, that a subsequent QFT will hand over to us just what we have been looking for!

[1]: https://2.bp.blogspot.com/-nj954YSSNqU/VtGIro8VoSI/AAAAAAAAAR0/yQ9Tgn7CcjM/s480/QFT.png
