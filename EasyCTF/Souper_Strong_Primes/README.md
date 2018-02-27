# Souper Strong Primes

## Challenge description

```
Technically I used strong primes. But are they really strong in this case? They are big, but there might still be an issue here. n.txt e.txt c.txt
```
[n.txt](https://raw.githubusercontent.com/EasyCTF/easyctf-iv-problems/master/souper_strong_primes/n.txt)
[e.txt](https://raw.githubusercontent.com/EasyCTF/easyctf-iv-problems/master/souper_strong_primes/e.txt)
[c.txt](https://raw.githubusercontent.com/EasyCTF/easyctf-iv-problems/master/souper_strong_primes/c.txt)

## Strong primes

Looking at **n**, we can see that it is **400,000 bits long**, which makes bruteforce completely unusable. Let's dig into Wikipedia to learn more about strong primes:

**\<Wikipedia>**

### Definition in number theory
<p>In <a href="https://en.wikipedia.org/wiki/Number_theory" title="Number theory">number theory</a>, a <b>strong prime</b> is a prime number that is greater than the <a href="https://en.wikipedia.org/wiki/Arithmetic_mean" title="Arithmetic mean">arithmetic mean</a> of the nearest prime above and below (in other words, it's closer to the following than to the preceding prime). Or to put it algebraically, given a prime number <span class="mwe-math-element"><span class="mwe-math-mathml-inline mwe-math-mathml-a11y" style="display: none;"><math xmlns="http://www.w3.org/1998/Math/MathML"  alttext="{\displaystyle p_{n}}">
  <semantics>
    <mrow class="MJX-TeXAtom-ORD">
      <mstyle displaystyle="true" scriptlevel="0">
        <msub>
          <mi>p</mi>
          <mrow class="MJX-TeXAtom-ORD">
            <mi>n</mi>
          </mrow>
        </msub>
      </mstyle>
    </mrow>
    <annotation encoding="application/x-tex">{\displaystyle p_{n}}</annotation>
  </semantics>
</math></span><img src="https://wikimedia.org/api/rest_v1/media/math/render/svg/6f79dcba35ecde0d43fbb7c914165586166ce8c2" class="mwe-math-fallback-image-inline" aria-hidden="true" style="vertical-align: -0.671ex; margin-left: -0.089ex; width:2.477ex; height:2.009ex;" alt="p_{n}" /></span>, where <i>n</i> is its index in the ordered set of prime numbers, <span class="mwe-math-element"><span class="mwe-math-mathml-inline mwe-math-mathml-a11y" style="display: none;"><math xmlns="http://www.w3.org/1998/Math/MathML"  alttext="{\displaystyle p_{n}&gt;{{p_{n-1}+p_{n+1}} \over 2}}">
  <semantics>
    <mrow class="MJX-TeXAtom-ORD">
      <mstyle displaystyle="true" scriptlevel="0">
        <msub>
          <mi>p</mi>
          <mrow class="MJX-TeXAtom-ORD">
            <mi>n</mi>
          </mrow>
        </msub>
        <mo>&gt;</mo>
        <mrow class="MJX-TeXAtom-ORD">
          <mfrac>
            <mrow class="MJX-TeXAtom-ORD">
              <msub>
                <mi>p</mi>
                <mrow class="MJX-TeXAtom-ORD">
                  <mi>n</mi>
                  <mo>&#x2212;<!-- − --></mo>
                  <mn>1</mn>
                </mrow>
              </msub>
              <mo>+</mo>
              <msub>
                <mi>p</mi>
                <mrow class="MJX-TeXAtom-ORD">
                  <mi>n</mi>
                  <mo>+</mo>
                  <mn>1</mn>
                </mrow>
              </msub>
            </mrow>
            <mn>2</mn>
          </mfrac>
        </mrow>
      </mstyle>
    </mrow>
    <annotation encoding="application/x-tex">{\displaystyle p_{n}&gt;{{p_{n-1}+p_{n+1}} \over 2}}</annotation>
  </semantics>
</math></span><img src="https://wikimedia.org/api/rest_v1/media/math/render/svg/487902078b76a2137fe28ed2a49b39aa2ccb6b8e" class="mwe-math-fallback-image-inline" aria-hidden="true" style="vertical-align: -1.838ex; margin-left: -0.089ex; width:18.229ex; height:5.176ex;" alt="p_{n}&gt;{{p_{{n-1}}+p_{{n+1}}} \over 2}" /></span>. The first few strong primes are</p>
<dl>
<dd><a href="https://en.wikipedia.org/wiki/11_(number)" title="11 (number)">11</a>, <a href="https://en.wikipedia.org/wiki/17_(number)" title="17 (number)">17</a>, <a href="https://en.wikipedia.org/wiki/29_(number)" title="29 (number)">29</a>, <a href="https://en.wikipedia.org/wiki/37_(number)" title="37 (number)">37</a>, <a href="https://en.wikipedia.org/wiki/41_(number)" title="41 (number)">41</a>, <a href="https://en.wikipedia.org/wiki/59_(number)" title="59 (number)">59</a>, <a href="https://en.wikipedia.org/wiki/67_(number)" title="67 (number)">67</a>, <a href="https://en.wikipedia.org/wiki/71_(number)" title="71 (number)">71</a>, <a href="https://en.wikipedia.org/wiki/79_(number)" title="79 (number)">79</a>, <a href="https://en.wikipedia.org/wiki/97_(number)" title="97 (number)">97</a>, <a href="https://en.wikipedia.org/wiki/101_(number)" title="101 (number)">101</a>, <a href="https://en.wikipedia.org/wiki/107_(number)" title="107 (number)">107</a>, <a href="https://en.wikipedia.org/wiki/127_(number)" title="127 (number)">127</a>, <a href="https://en.wikipedia.org/wiki/137_(number)" title="137 (number)">137</a>, <a href="https://en.wikipedia.org/wiki/149_(number)" title="149 (number)">149</a>, <a href="https://en.wikipedia.org/wiki/163_(number)" title="163 (number)">163</a>, <a href="https://en.wikipedia.org/wiki/179_(number)" title="179 (number)">179</a>, <a href="https://en.wikipedia.org/wiki/191_(number)" title="191 (number)">191</a>, <a href="https://en.wikipedia.org/wiki/197_(number)" title="197 (number)">197</a>, <a href="https://en.wikipedia.org/wiki/223_(number)" title="223 (number)">223</a>, <a href="https://en.wikipedia.org/wiki/227_(number)" title="227 (number)">227</a>, <a href="https://en.wikipedia.org/wiki/239_(number)" title="239 (number)">239</a>, <a href="https://en.wikipedia.org/wiki/251_(number)" title="251 (number)">251</a>, <a href="https://en.wikipedia.org/wiki/269_(number)" title="269 (number)">269</a>, <a href="https://en.wikipedia.org/wiki/277_(number)" title="277 (number)">277</a>, 281, 307, 311, 331, 347, 367, 379, 397, 419, 431, 439, 457, 461, 479, 487, 499 (sequence <span class="nowrap"><a href="//oeis.org/A051634" class="extiw" title="oeis:A051634">A051634</a></span> in the <a href="https://en.wikipedia.org/wiki/On-Line_Encyclopedia_of_Integer_Sequences" title="On-Line Encyclopedia of Integer Sequences">OEIS</a>).</dd>
</dl>
<p>For example, 17 is the seventh prime. The sixth and eighth primes, 13 and 19, add up to 32, and half that is 16. That is less than 17, thus 17 is a strong prime.</p>
<p>In a <a href="https://en.wikipedia.org/wiki/Twin_prime" title="Twin prime">twin prime</a> pair (<i>p</i>, <i>p</i> + 2) with <i>p</i> &gt; 5, <i>p</i> is always a strong prime, since 3 must divide <i>p</i> − 2 which cannot be prime.</p>
<p>It is possible for a prime to be a strong prime both in the cryptographic sense and the number theoretic sense. For the sake of illustration, 439351292910452432574786963588089477522344331 is a strong prime in the number theoretic sense because the arithmetic mean of its two neighboring primes is 62 less. Without the aid of a computer, this number would be a strong prime in the cryptographic sense because 439351292910452432574786963588089477522344330 has the large prime factor 1747822896920092227343 (and in turn the number one less than that has the large prime factor 1683837087591611009), 439351292910452432574786963588089477522344332 has the large prime factor 864608136454559457049 (and in turn the number one less than that has the large prime factor 105646155480762397). Even using algorithms more advanced than <a href="https://en.wikipedia.org/wiki/Trial_division" title="Trial division">trial division</a>, these numbers would be difficult to factor by hand. For a modern <a href="https://en.wikipedia.org/wiki/Computer_algebra_system" title="Computer algebra system">computer algebra system</a>, these numbers can be factored almost instantaneously. A <a href="https://en.wikipedia.org/wiki/Cryptographically_strong" class="mw-redirect" title="Cryptographically strong">cryptographically strong</a> prime has to be much larger than this example.</p>

### Definition in cryptography

<p>In <a href="https://en.wikipedia.org/wiki/Cryptography" title="Cryptography">cryptography</a>, a prime number <span class="mwe-math-element"><span class="mwe-math-mathml-inline mwe-math-mathml-a11y" style="display: none;"><math xmlns="http://www.w3.org/1998/Math/MathML"  alttext="{\displaystyle p}">
  <semantics>
    <mrow class="MJX-TeXAtom-ORD">
      <mstyle displaystyle="true" scriptlevel="0">
        <mi>p</mi>
      </mstyle>
    </mrow>
    <annotation encoding="application/x-tex">{\displaystyle p}</annotation>
  </semantics>
</math></span><img src="https://wikimedia.org/api/rest_v1/media/math/render/svg/81eac1e205430d1f40810df36a0edffdc367af36" class="mwe-math-fallback-image-inline" aria-hidden="true" style="vertical-align: -0.671ex; margin-left: -0.089ex; width:1.259ex; height:2.009ex;" alt="p" /></span> is <i>strong</i> if the following conditions are satisfied.<sup id="cite_ref-rivest_1-0" class="reference"><a href="#cite_note-rivest-1">[1]</a></sup></p>
<ul>
<li><span class="mwe-math-element"><span class="mwe-math-mathml-inline mwe-math-mathml-a11y" style="display: none;"><math xmlns="http://www.w3.org/1998/Math/MathML"  alttext="{\displaystyle p}">
  <semantics>
    <mrow class="MJX-TeXAtom-ORD">
      <mstyle displaystyle="true" scriptlevel="0">
        <mi>p</mi>
      </mstyle>
    </mrow>
    <annotation encoding="application/x-tex">{\displaystyle p}</annotation>
  </semantics>
</math></span><img src="https://wikimedia.org/api/rest_v1/media/math/render/svg/81eac1e205430d1f40810df36a0edffdc367af36" class="mwe-math-fallback-image-inline" aria-hidden="true" style="vertical-align: -0.671ex; margin-left: -0.089ex; width:1.259ex; height:2.009ex;" alt="p" /></span> is sufficiently large to be useful in cryptography; typically this requires <span class="mwe-math-element"><span class="mwe-math-mathml-inline mwe-math-mathml-a11y" style="display: none;"><math xmlns="http://www.w3.org/1998/Math/MathML"  alttext="{\displaystyle p}">
  <semantics>
    <mrow class="MJX-TeXAtom-ORD">
      <mstyle displaystyle="true" scriptlevel="0">
        <mi>p</mi>
      </mstyle>
    </mrow>
    <annotation encoding="application/x-tex">{\displaystyle p}</annotation>
  </semantics>
</math></span><img src="https://wikimedia.org/api/rest_v1/media/math/render/svg/81eac1e205430d1f40810df36a0edffdc367af36" class="mwe-math-fallback-image-inline" aria-hidden="true" style="vertical-align: -0.671ex; margin-left: -0.089ex; width:1.259ex; height:2.009ex;" alt="p" /></span> to be too large for plausible computational resources to enable a <a href="https://en.wikipedia.org/wiki/Cryptanalyst" class="mw-redirect" title="Cryptanalyst">cryptanalyst</a> to <a href="https://en.wikipedia.org/wiki/Factorisation" class="mw-redirect" title="Factorisation">factorise</a> products of <span class="mwe-math-element"><span class="mwe-math-mathml-inline mwe-math-mathml-a11y" style="display: none;"><math xmlns="http://www.w3.org/1998/Math/MathML"  alttext="{\displaystyle p}">
  <semantics>
    <mrow class="MJX-TeXAtom-ORD">
      <mstyle displaystyle="true" scriptlevel="0">
        <mi>p</mi>
      </mstyle>
    </mrow>
    <annotation encoding="application/x-tex">{\displaystyle p}</annotation>
  </semantics>
</math></span><img src="https://wikimedia.org/api/rest_v1/media/math/render/svg/81eac1e205430d1f40810df36a0edffdc367af36" class="mwe-math-fallback-image-inline" aria-hidden="true" style="vertical-align: -0.671ex; margin-left: -0.089ex; width:1.259ex; height:2.009ex;" alt="p" /></span> multiplied by other strong primes.</li>
<li><span class="mwe-math-element"><span class="mwe-math-mathml-inline mwe-math-mathml-a11y" style="display: none;"><math xmlns="http://www.w3.org/1998/Math/MathML"  alttext="{\displaystyle p-1}">
  <semantics>
    <mrow class="MJX-TeXAtom-ORD">
      <mstyle displaystyle="true" scriptlevel="0">
        <mi>p</mi>
        <mo>&#x2212;<!-- − --></mo>
        <mn>1</mn>
      </mstyle>
    </mrow>
    <annotation encoding="application/x-tex">{\displaystyle p-1}</annotation>
  </semantics>
</math></span><img src="https://wikimedia.org/api/rest_v1/media/math/render/svg/f356ae51988add41a7da343e6b6d48fa968da162" class="mwe-math-fallback-image-inline" aria-hidden="true" style="vertical-align: -0.671ex; margin-left: -0.089ex; width:5.262ex; height:2.509ex;" alt="p-1" /></span> has large prime factors. That is, <span class="mwe-math-element"><span class="mwe-math-mathml-inline mwe-math-mathml-a11y" style="display: none;"><math xmlns="http://www.w3.org/1998/Math/MathML"  alttext="{\displaystyle p=a_{1}q_{1}+1}">
  <semantics>
    <mrow class="MJX-TeXAtom-ORD">
      <mstyle displaystyle="true" scriptlevel="0">
        <mi>p</mi>
        <mo>=</mo>
        <msub>
          <mi>a</mi>
          <mrow class="MJX-TeXAtom-ORD">
            <mn>1</mn>
          </mrow>
        </msub>
        <msub>
          <mi>q</mi>
          <mrow class="MJX-TeXAtom-ORD">
            <mn>1</mn>
          </mrow>
        </msub>
        <mo>+</mo>
        <mn>1</mn>
      </mstyle>
    </mrow>
    <annotation encoding="application/x-tex">{\displaystyle p=a_{1}q_{1}+1}</annotation>
  </semantics>
</math></span><img src="https://wikimedia.org/api/rest_v1/media/math/render/svg/8a0d132df7dc5516956b0eed475a0e8da16ec0e0" class="mwe-math-fallback-image-inline" aria-hidden="true" style="vertical-align: -0.671ex; margin-left: -0.089ex; width:12.735ex; height:2.509ex;" alt="p=a_{1}q_{1}+1" /></span> for some integer <span class="mwe-math-element"><span class="mwe-math-mathml-inline mwe-math-mathml-a11y" style="display: none;"><math xmlns="http://www.w3.org/1998/Math/MathML"  alttext="{\displaystyle a_{1}}">
  <semantics>
    <mrow class="MJX-TeXAtom-ORD">
      <mstyle displaystyle="true" scriptlevel="0">
        <msub>
          <mi>a</mi>
          <mrow class="MJX-TeXAtom-ORD">
            <mn>1</mn>
          </mrow>
        </msub>
      </mstyle>
    </mrow>
    <annotation encoding="application/x-tex">{\displaystyle a_{1}}</annotation>
  </semantics>
</math></span><img src="https://wikimedia.org/api/rest_v1/media/math/render/svg/bbf42ecda092975c9c69dae84e16182ba5fe2e07" class="mwe-math-fallback-image-inline" aria-hidden="true" style="vertical-align: -0.671ex; width:2.284ex; height:2.009ex;" alt="a_{1}" /></span> and large prime <span class="mwe-math-element"><span class="mwe-math-mathml-inline mwe-math-mathml-a11y" style="display: none;"><math xmlns="http://www.w3.org/1998/Math/MathML"  alttext="{\displaystyle q_{1}}">
  <semantics>
    <mrow class="MJX-TeXAtom-ORD">
      <mstyle displaystyle="true" scriptlevel="0">
        <msub>
          <mi>q</mi>
          <mrow class="MJX-TeXAtom-ORD">
            <mn>1</mn>
          </mrow>
        </msub>
      </mstyle>
    </mrow>
    <annotation encoding="application/x-tex">{\displaystyle q_{1}}</annotation>
  </semantics>
</math></span><img src="https://wikimedia.org/api/rest_v1/media/math/render/svg/9daa41f6e8f78ea6bb5711d7ac97901ce564b94e" class="mwe-math-fallback-image-inline" aria-hidden="true" style="vertical-align: -0.671ex; width:2.091ex; height:2.009ex;" alt="q_{1}" /></span>.</li>
<li><span class="mwe-math-element"><span class="mwe-math-mathml-inline mwe-math-mathml-a11y" style="display: none;"><math xmlns="http://www.w3.org/1998/Math/MathML"  alttext="{\displaystyle q_{1}-1}">
  <semantics>
    <mrow class="MJX-TeXAtom-ORD">
      <mstyle displaystyle="true" scriptlevel="0">
        <msub>
          <mi>q</mi>
          <mrow class="MJX-TeXAtom-ORD">
            <mn>1</mn>
          </mrow>
        </msub>
        <mo>&#x2212;<!-- − --></mo>
        <mn>1</mn>
      </mstyle>
    </mrow>
    <annotation encoding="application/x-tex">{\displaystyle q_{1}-1}</annotation>
  </semantics>
</math></span><img src="https://wikimedia.org/api/rest_v1/media/math/render/svg/ec09c3f9a047bf5b1cf4e4fcd5f34c161ea098bb" class="mwe-math-fallback-image-inline" aria-hidden="true" style="vertical-align: -0.671ex; width:6.094ex; height:2.509ex;" alt="q_{1}-1" /></span> has large prime factors. That is, <span class="mwe-math-element"><span class="mwe-math-mathml-inline mwe-math-mathml-a11y" style="display: none;"><math xmlns="http://www.w3.org/1998/Math/MathML"  alttext="{\displaystyle q_{1}=a_{2}q_{2}+1}">
  <semantics>
    <mrow class="MJX-TeXAtom-ORD">
      <mstyle displaystyle="true" scriptlevel="0">
        <msub>
          <mi>q</mi>
          <mrow class="MJX-TeXAtom-ORD">
            <mn>1</mn>
          </mrow>
        </msub>
        <mo>=</mo>
        <msub>
          <mi>a</mi>
          <mrow class="MJX-TeXAtom-ORD">
            <mn>2</mn>
          </mrow>
        </msub>
        <msub>
          <mi>q</mi>
          <mrow class="MJX-TeXAtom-ORD">
            <mn>2</mn>
          </mrow>
        </msub>
        <mo>+</mo>
        <mn>1</mn>
      </mstyle>
    </mrow>
    <annotation encoding="application/x-tex">{\displaystyle q_{1}=a_{2}q_{2}+1}</annotation>
  </semantics>
</math></span><img src="https://wikimedia.org/api/rest_v1/media/math/render/svg/785c788a6fbdd02aa208d299f1aa26580c91deaa" class="mwe-math-fallback-image-inline" aria-hidden="true" style="vertical-align: -0.671ex; width:13.568ex; height:2.509ex;" alt="q_{1}=a_{2}q_{2}+1" /></span> for some integer <span class="mwe-math-element"><span class="mwe-math-mathml-inline mwe-math-mathml-a11y" style="display: none;"><math xmlns="http://www.w3.org/1998/Math/MathML"  alttext="{\displaystyle a_{2}}">
  <semantics>
    <mrow class="MJX-TeXAtom-ORD">
      <mstyle displaystyle="true" scriptlevel="0">
        <msub>
          <mi>a</mi>
          <mrow class="MJX-TeXAtom-ORD">
            <mn>2</mn>
          </mrow>
        </msub>
      </mstyle>
    </mrow>
    <annotation encoding="application/x-tex">{\displaystyle a_{2}}</annotation>
  </semantics>
</math></span><img src="https://wikimedia.org/api/rest_v1/media/math/render/svg/270580da7333505d9b73697417d0543c43c98b9f" class="mwe-math-fallback-image-inline" aria-hidden="true" style="vertical-align: -0.671ex; width:2.284ex; height:2.009ex;" alt="a_{2}" /></span> and large prime <span class="mwe-math-element"><span class="mwe-math-mathml-inline mwe-math-mathml-a11y" style="display: none;"><math xmlns="http://www.w3.org/1998/Math/MathML"  alttext="{\displaystyle q_{2}}">
  <semantics>
    <mrow class="MJX-TeXAtom-ORD">
      <mstyle displaystyle="true" scriptlevel="0">
        <msub>
          <mi>q</mi>
          <mrow class="MJX-TeXAtom-ORD">
            <mn>2</mn>
          </mrow>
        </msub>
      </mstyle>
    </mrow>
    <annotation encoding="application/x-tex">{\displaystyle q_{2}}</annotation>
  </semantics>
</math></span><img src="https://wikimedia.org/api/rest_v1/media/math/render/svg/fd2d05084feb02b8ba29b0673440fb673b102589" class="mwe-math-fallback-image-inline" aria-hidden="true" style="vertical-align: -0.671ex; width:2.091ex; height:2.009ex;" alt="q_{2}" /></span>.</li>
<li><span class="mwe-math-element"><span class="mwe-math-mathml-inline mwe-math-mathml-a11y" style="display: none;"><math xmlns="http://www.w3.org/1998/Math/MathML"  alttext="{\displaystyle p+1}">
  <semantics>
    <mrow class="MJX-TeXAtom-ORD">
      <mstyle displaystyle="true" scriptlevel="0">
        <mi>p</mi>
        <mo>+</mo>
        <mn>1</mn>
      </mstyle>
    </mrow>
    <annotation encoding="application/x-tex">{\displaystyle p+1}</annotation>
  </semantics>
</math></span><img src="https://wikimedia.org/api/rest_v1/media/math/render/svg/5885ec01d3b5670fd5f88847f32da2b3dd62f60c" class="mwe-math-fallback-image-inline" aria-hidden="true" style="vertical-align: -0.671ex; margin-left: -0.089ex; width:5.262ex; height:2.509ex;" alt="p+1" /></span> has large prime factors. That is, <span class="mwe-math-element"><span class="mwe-math-mathml-inline mwe-math-mathml-a11y" style="display: none;"><math xmlns="http://www.w3.org/1998/Math/MathML"  alttext="{\displaystyle p=a_{3}q_{3}-1}">
  <semantics>
    <mrow class="MJX-TeXAtom-ORD">
      <mstyle displaystyle="true" scriptlevel="0">
        <mi>p</mi>
        <mo>=</mo>
        <msub>
          <mi>a</mi>
          <mrow class="MJX-TeXAtom-ORD">
            <mn>3</mn>
          </mrow>
        </msub>
        <msub>
          <mi>q</mi>
          <mrow class="MJX-TeXAtom-ORD">
            <mn>3</mn>
          </mrow>
        </msub>
        <mo>&#x2212;<!-- − --></mo>
        <mn>1</mn>
      </mstyle>
    </mrow>
    <annotation encoding="application/x-tex">{\displaystyle p=a_{3}q_{3}-1}</annotation>
  </semantics>
</math></span><img src="https://wikimedia.org/api/rest_v1/media/math/render/svg/733dbb9fd344ffca7a8dc56a98d42b9d096eba2d" class="mwe-math-fallback-image-inline" aria-hidden="true" style="vertical-align: -0.671ex; margin-left: -0.089ex; width:12.735ex; height:2.509ex;" alt="p=a_{3}q_{3}-1" /></span> for some integer <span class="mwe-math-element"><span class="mwe-math-mathml-inline mwe-math-mathml-a11y" style="display: none;"><math xmlns="http://www.w3.org/1998/Math/MathML"  alttext="{\displaystyle a_{3}}">
  <semantics>
    <mrow class="MJX-TeXAtom-ORD">
      <mstyle displaystyle="true" scriptlevel="0">
        <msub>
          <mi>a</mi>
          <mrow class="MJX-TeXAtom-ORD">
            <mn>3</mn>
          </mrow>
        </msub>
      </mstyle>
    </mrow>
    <annotation encoding="application/x-tex">{\displaystyle a_{3}}</annotation>
  </semantics>
</math></span><img src="https://wikimedia.org/api/rest_v1/media/math/render/svg/602d08dd865689204f563ce6f0de095c8ca67410" class="mwe-math-fallback-image-inline" aria-hidden="true" style="vertical-align: -0.671ex; width:2.284ex; height:2.009ex;" alt="a_{3}" /></span> and large prime <span class="mwe-math-element"><span class="mwe-math-mathml-inline mwe-math-mathml-a11y" style="display: none;"><math xmlns="http://www.w3.org/1998/Math/MathML"  alttext="{\displaystyle q_{3}}">
  <semantics>
    <mrow class="MJX-TeXAtom-ORD">
      <mstyle displaystyle="true" scriptlevel="0">
        <msub>
          <mi>q</mi>
          <mrow class="MJX-TeXAtom-ORD">
            <mn>3</mn>
          </mrow>
        </msub>
      </mstyle>
    </mrow>
    <annotation encoding="application/x-tex">{\displaystyle q_{3}}</annotation>
  </semantics>
</math></span><img src="https://wikimedia.org/api/rest_v1/media/math/render/svg/c188711ffce607c8dd7504a6dcb52196e8b670b8" class="mwe-math-fallback-image-inline" aria-hidden="true" style="vertical-align: -0.671ex; width:2.091ex; height:2.009ex;" alt="q_{3}" /></span></li>
</ul>

### Application of strong primes in cryptography

#### Factoring-based cryptosystems
<p>Some people suggest that in the <a href="https://en.wikipedia.org/wiki/Key_generation" title="Key generation">key generation</a> process in <a href="https://en.wikipedia.org/wiki/RSA_(algorithm)" class="mw-redirect" title="RSA (algorithm)">RSA</a> cryptosystems, the modulus <span class="mwe-math-element"><span class="mwe-math-mathml-inline mwe-math-mathml-a11y" style="display: none;"><math xmlns="http://www.w3.org/1998/Math/MathML"  alttext="{\displaystyle n}">
  <semantics>
    <mrow class="MJX-TeXAtom-ORD">
      <mstyle displaystyle="true" scriptlevel="0">
        <mi>n</mi>
      </mstyle>
    </mrow>
    <annotation encoding="application/x-tex">{\displaystyle n}</annotation>
  </semantics>
</math></span><img src="https://wikimedia.org/api/rest_v1/media/math/render/svg/a601995d55609f2d9f5e233e36fbe9ea26011b3b" class="mwe-math-fallback-image-inline" aria-hidden="true" style="vertical-align: -0.338ex; width:1.395ex; height:1.676ex;" alt="n" /></span> should be chosen as the product of two strong primes. This makes the factorization of <span class="mwe-math-element"><span class="mwe-math-mathml-inline mwe-math-mathml-a11y" style="display: none;"><math xmlns="http://www.w3.org/1998/Math/MathML"  alttext="{\displaystyle n=pq}">
  <semantics>
    <mrow class="MJX-TeXAtom-ORD">
      <mstyle displaystyle="true" scriptlevel="0">
        <mi>n</mi>
        <mo>=</mo>
        <mi>p</mi>
        <mi>q</mi>
      </mstyle>
    </mrow>
    <annotation encoding="application/x-tex">{\displaystyle n=pq}</annotation>
  </semantics>
</math></span><img src="https://wikimedia.org/api/rest_v1/media/math/render/svg/edd7540bf012670052b38c45bf043b5c8e6cd159" class="mwe-math-fallback-image-inline" aria-hidden="true" style="vertical-align: -0.671ex; width:6.732ex; height:2.009ex;" alt="n=pq" /></span> using <a href="https://en.wikipedia.org/wiki/Pollard%27s_p_-_1_algorithm" class="mw-redirect" title="Pollard's p - 1 algorithm">Pollard's <i>p</i>&#160;−&#160;1 algorithm</a> computationally infeasible. For this reason, strong primes are required by the <a href="/w/index.php?title=ANSI_X9.31&amp;action=edit&amp;redlink=1" class="new" title="ANSI X9.31 (page does not exist)">ANSI X9.31</a> standard for use in generating RSA keys for <a href="https://en.wikipedia.org/wiki/Digital_signature" title="Digital signature">digital signatures</a>. However, strong primes do not protect against modulus factorisation using newer algorithms such as <a href="https://en.wikipedia.org/wiki/Lenstra_elliptic_curve_factorization" class="mw-redirect" title="Lenstra elliptic curve factorization">Lenstra elliptic curve factorization</a> and <a href="https://en.wikipedia.org/wiki/Number_Field_Sieve" class="mw-redirect" title="Number Field Sieve">Number Field Sieve</a> algorithm. Given the additional cost of generating strong primes <a href="https://en.wikipedia.org/wiki/RSA_Security" title="RSA Security">RSA Security</a> do not currently recommend their use in <a href="https://en.wikipedia.org/wiki/Key_generation" title="Key generation">key generation</a>. Similar (and more technical) argument is also given by Rivest and Silverman.<sup id="cite_ref-rivest_1-1" class="reference"><a href="#cite_note-rivest-1">[1]</a></sup></p>

#### Discrete-logarithm-based cryptosystems

<p>It is shown by Stephen Pohlig and <a href="https://en.wikipedia.org/wiki/Martin_Hellman" title="Martin Hellman">Martin Hellman</a> in 1978 that if all the factors of <i>p-1</i> are less than <span class="mwe-math-element"><span class="mwe-math-mathml-inline mwe-math-mathml-a11y" style="display: none;"><math xmlns="http://www.w3.org/1998/Math/MathML"  alttext="{\displaystyle \log ^{c}p}">
  <semantics>
    <mrow class="MJX-TeXAtom-ORD">
      <mstyle displaystyle="true" scriptlevel="0">
        <msup>
          <mi>log</mi>
          <mrow class="MJX-TeXAtom-ORD">
            <mi>c</mi>
          </mrow>
        </msup>
        <mo>&#x2061;<!-- ⁡ --></mo>
        <mi>p</mi>
      </mstyle>
    </mrow>
    <annotation encoding="application/x-tex">{\displaystyle \log ^{c}p}</annotation>
  </semantics>
</math></span><img src="https://wikimedia.org/api/rest_v1/media/math/render/svg/0847acfa581e1a8291b836e6c3bf2be31b687a74" class="mwe-math-fallback-image-inline" aria-hidden="true" style="vertical-align: -0.671ex; width:5.472ex; height:2.676ex;" alt="\log ^{c}p" /></span>, then the problem of solving <a href="https://en.wikipedia.org/wiki/Discrete_logarithm" title="Discrete logarithm">discrete logarithm</a> modulo <i>p</i> is in <a href="https://en.wikipedia.org/wiki/P_%3D_NP_problem" class="mw-redirect" title="P = NP problem">P</a>. Therefore, for cryptosystems based on discrete logarithm, such as <a href="https://en.wikipedia.org/wiki/Digital_Signature_Algorithm" title="Digital Signature Algorithm">DSA</a>, it is required that <i>p-1</i> have at least one large prime factor.</p>


**\</Wikipedia>**

So basically, using two strong primes as defined for **cryptography** as the factors of **n** in **RSA** is super-duper secure. Ugh.

The only thing that would make the challenge solvable is if strong primes from number theory were used, specifically **twin primes**.

## Factoring n

To figure that out, we use sage to solve the equation **p(p + 2) = n**:

```python
var('p')
solve([p * (p + 2) == n], p)
```

We actually find a value for **p**! This enables us to find **q**, since **q = n / p**, or even easier, **q = p + 2**.

## Decrypting the ciphertext

We started trying to decrypt the ciphertext, but after **more than 1 hour** we still weren't able to get a result. The key and the cipher were simply too big.

Our computers being what they are (*hint: not really all that powerful*), we had to figure out a different way, and stumbled upon [this link](https://www.di-mgt.com.au/crt_rsa.html) (*TL;DR we can use the Chinese Remainder Theorem to speed up our calculations*).

We then implemented the following program:

```python
from gmpy2 import *

e = int(open('e.txt').read())
c = int(open('c.txt').read())
p = int(open('p.txt').read())
q = int(open('q.txt').read())

dp = invert(e, p - 1)
dq = invert(e, q - 1)
qinv = invert(q, p)

m1 = pow(c, dp, p)
m2 = pow(c, dq, q)
h = (qinv * (m1 - m2)) % p 

m = m2 + h * q

print m
```

which, after about **40 minutes**, gave us the flag!

**Flag: easyctf{Str0ng_prim3s_n0t_s0_str000ng}**




