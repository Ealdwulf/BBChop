<TeXmacs|1.0.6.11>

<style|generic>

<\body>
  <doc-data|<\doc-title>
    A Bayesian Binary Search algorithm\ 

    for locating non-deterministic faults
  </doc-title>|<doc-author-data|<author-name|Ealdwulf Wuffinga>>|>

  \;

  <subsection|Introduction>

  Suppose you find a fault in your code, and want to know in what version it
  was introduced. It is common to use the binary search algorithm to answer
  this question. However, binary search requires at test which can tell us
  whether the fault is present or absent. If the fault is an intermittent or
  non-deterministic one, we only have a weaker test - if we observe the
  fault, it is certainly present, but if we do not observe it, it might still
  be present.\ 

  \;

  <subsection|Calculations (discrete case)>

  <subsubsection|Definitions>

  <\small-table>
    <block|<tformat|<table|<row|<cell|<with|mode|math|r<rsub|k>>>|<cell|failure
    rate at location <with|mode|math|k>>>|<row|<cell|<with|mode|math|l<rsub|1>>..<with|mode|math|l<rsub|N>>>|<cell|locations>>|<row|<cell|<with|mode|math|L>>|<cell|(putative)
    location of bug>>>>>

    \;
  <|small-table>
    \;
  </small-table>

  A test at location <with|mode|math|l<rsub|k>> detects with probability
  <with|mode|math|r<rsub|k>> if <with|mode|math|L\<gtr\>k>, otheriwse does
  not detect.

  Initialy, we shall assume that <with|mode|math|r<rsub|k>=r> for all
  <with|mode|math|k>. Later we shall show how to relax this assumption

  <subsubsection|Assuming constant <with|mode|math|r> at all locations>

  Our evidence <with|mode|math|E> is completely represented by:

  <small-table|<block|<tformat|<table|<row|<cell|<with|mode|math|t<rsub|k>,
  k\<in\>1\<ldots\>N>>|<cell|number of tests at locations k which did not
  detect>>|<row|<cell|<with|mode|math|d<rsub|k>,k\<in\>1\<ldots\>N>>|<cell|number
  of tests at locations k which did detect>>>>>|>\ 

  Our prior belief is <with|mode|math|P(L=l<rsub|k>)=bl<rsub|k>> (ie,
  arbitrary) and <with|mode|math|P(a\<less\>r\<less\>b)=b-a> (ie, uniform
  p.d.f. on r in 0..1)

  We can write down <with|mode|math|P(E\|L,r), as follows:>

  <\equation*>
    P(E\|L,r) = <choice|<tformat|<table|<row|<cell|0>|<cell|if
    d<rsub|k>\<neq\>0 for any k\<less\>L>>|<row|<cell|>|<cell|>>|<row|<cell|<big|prod><rsub|i=L\<ldots\>N>
    (1-r)<rsup|t<rsub|i>> r<rsup|d<rsub|i>>>|<cell|otherwise>>>>>
  </equation*>

  \;

  \ (NB: this assumes we know the order in which the detections and
  non-detections occurred, otherwise there is a term
  <math|<left|(><stack|<tformat|<table|<row|<cell|t<rsub|i>+d<rsub|i>>>|<row|<cell|t<rsub|i>>>>>><right|)>>.
  (fixme: wouldn't this drop out in te end anyway?)

  We want <with|mode|math|P(L\|E)>. To get this we must marginalise
  <with|mode|math|P(L,r\|E)>.

  <\equation*>
    P(L\|E) = <big|int><rsub|r\<in\>0\<ldots\>1>P(L,r\|E)
  </equation*>

  \;

  By Bayes theorem,

  <\equation*>
    P(L,r\|E) = \ <frac|P(E\|L,r)P(L,r)|P(E)>
  </equation*>

  \;

  <with|mode|math|P(L,r)> is just the prior <with|mode|math|P(L)P(r)>.

  <with|mode|math|P(E)> must be found by marginalising
  <with|mode|math|pdf(E,L,r)> over both <with|mode|math|L> and
  <with|mode|math|r>

  <\equation*>
    pdf(E,L,r) = P(E\|L,r)P(L)pdf(r)
  </equation*>

  <\eqnarray*>
    <tformat|<table|<row|<cell|<htab|5mm><tabular|<tformat|<table|<row|<cell|P(E)>|<cell|=>|<cell|<big|sum><rsub|i\<in\>1\<ldots\>N><big|int><rsub|r=0\<ldots\>1>P(E,L,r)dr>>|<row|<cell|>|<cell|>|<cell|>>|<row|<cell|>|<cell|=>|<cell|<big|sum><rsub|i\<in\>1\<ldots\>N><big|int><rsub|r=0\<ldots\>1>P(E\|L,r)P(L)pdf(r)dr>>>>>>|<cell|>|<cell|>>>>
  </eqnarray*>

  \;

  define <with|mode|math|g(E,L)> as the integral:

  <\equation*>
    g(E,L)=<big|int><rsub|r=0\<ldots\>1>P(E\|L,r)P(L)pdf(r)
  </equation*>

  <\equation*>
    g(E,L) = <choice|<tformat|<table|<row|<cell|0>|<cell|if d<rsub|k>\<neq\>0
    for any k\<less\>L>>|<row|<cell|<big|int><rsub|r=0\<ldots\>1><big|prod><rsub|i=L\<ldots\>N>
    (1-r)<rsup|t<rsub|i>> r<rsup|d<rsub|i>>P(L)dr>|<cell|otherwise>>>>>
  </equation*>

  \;

  define <with|mode|math|T<rsub|l>=<big|sum><rsub|i=L\<ldots\>N>t<rsub|i>>
  and <with|mode|math|D<rsub|l>=<big|sum><rsub|i=L\<ldots\>N>d<rsub|i>>. Then
  <with|mode|math|g(E,L) >is:

  <\equation*>
    g(E,L)=<choice|<tformat|<table|<row|<cell|0>|<cell|if d<rsub|k>\<neq\>0
    for any k\<less\>L>>|<row|<cell|<big|int><rsub|r=0\<ldots\>1>
    (1-r)<rsup|T<rsub|L>> r<rsup|D<rsub|L><rsub|i>>P(L)dr>|<cell|otherwise>>>>>
  </equation*>

  <\equation*>
    g(E,L)=<choice|<tformat|<table|<row|<cell|0>|<cell|if d<rsub|k>\<neq\>0
    for any k\<less\>L>>|<row|<cell|Beta(D<rsub|L>+1,T<rsub|L>+1)P(L)>|<cell|otherwise>>>>>
  </equation*>

  <\equation*>
    P(E) = <big|sum><rsub|i\<in\>1\<ldots\>N>g(E,i)
  </equation*>

  In fact, <with|mode|math|g(E,L)> is also, by the same reasoning,
  <with|mode|math|P(E\|L,r)P(L,r)> marginalised over <with|mode|math|r>,
  which is

  the remaining piece we need to write down <with|mode|math|P(E\|L)>:

  <\equation*>
    P(E\|L)=<frac|g(E,L)|<big|sum><rsub|i\<in\>1\<ldots\>N>g(E,i)<rsub|>>
  </equation*>

  \;

  \;

  \;

  We also need to calculate <with|mode|math|P(D<rsub|i>\|E)>, the probability
  that a measurement at <with|mode|math|l<rsub|i>> will detect given the
  evidence E collected so far.\ 

  <\equation*>
    <with|mode|text|<with|mode|math|P(D<rsub|i>\|E)=<frac|P(D<rsub|i>,E)|P(E)>>>
  </equation*>

  We already know how to calculate <with|mode|math|P(E)>:
  <with|mode|math|P(D<rsub|i>,E)> is the same except with another detection
  added to <with|mode|math|d<rsub|i>>.\ 

  <subsubsection|Multiple <with|mode|math|r<rsub|i>>>

  If we cannot assume that <with|mode|math|r> is constant at all locations,
  there are a couple of possibilities:

  <\itemize-minus>
    <item>Assume nothing about the <with|mode|math|r<rsub|i>>

    <item>take the possibility that <with|mode|math|r> is constant into
    account, by assigning some prior probability to the hypothesis that this
    is the case.
  </itemize-minus>

  The latter is the best course of action if we have some reason for
  believing that constant <with|mode|math|r> is more likely than would be
  represented by an independent uniform distribution of all the
  <with|mode|math|r<rsub|i>>. One reason for proceeding in this fashion is
  that an intermittent fault is likely to have some underlying rate, constant
  in all locations, but in some locations it may be (partially) obscured.

  \;

  <subsubsection|Independent <with|mode|math|r<rsub|i>>>

  In the case where we assume nothing about the <with|mode|math|r<rsub|i>>,
  we assign them each an independent uniform prior in 0..1.

  \ <with|mode|math|P(E\|L,r<rsub|0>\<ldots\>r<rsub|N>) is now:>

  <\equation*>
    P(E\|L,r<rsub|0>\<ldots\>r<rsub|N>) =
    <choice|<tformat|<table|<row|<cell|0>|<cell|if d<rsub|k>\<neq\>0 for any
    k\<less\>L>>|<row|<cell|w>|<cell|>>|<row|<cell|<big|prod><rsub|i=L\<ldots\>N>
    (1-r<rsub|i>)<rsup|t<rsub|i>> r<rsub|i><rsup|d<rsub|i>>>|<cell|otherwise>>>>>
  </equation*>

  \;

  <\equation*>
    P(L\|E) = <big|int><rsub|r<rsub|0>>\<ldots\>.<big|int><rsub|r<rsub|N>>P(L,r<rsub|0>\<ldots\>.r<rsub|N>\|E)
  </equation*>

  The above calculation all works out the same, with the extra integrals
  everywhere, and we get:

  <\equation*>
    <\with|mode|text>
      <\equation*>
        g(E,L)=<choice|<tformat|<table|<row|<cell|0>|<cell|if
        d<rsub|k>\<neq\>0 for any k\<less\>L>>|<row|<cell|<big|prod><rsub|i\<in\>L\<ldots\>N>Beta(d<rsub|i>+1,t<rsub|i>+1)P(L)>|<cell|otherwise>>>>>
      </equation*>
    </with>
  </equation*>

  \;

  <subsubsection|Two models for <with|mode|math|r>>

  Call the assumption that the <with|mode|math|r<rsub|i>> are independent
  <with|mode|math|M<rsub|I>> and the assumtion that the
  <with|mode|math|r<rsub|i>> are the same, <with|mode|math|M<rsub|=<rsub|>>>.
  Now, suppose we assign some prior probabilities to the two models such that
  <with|mode|math|P(M<rsub|I>)+P(M<rsub|=>)=1.> We want to calculate the
  probabilities <with|mode|math|P(L=l<rsub|i>\|E)> under these assumptions.

  <\equation*>
    P(L\|E)=P(L\|E,M<rsub|I>)P(M<rsub|I>\|E)+P(L<rsub|>\|E,M<rsub|=>)P(M<rsub|=>\|E)
  </equation*>

  \;

  We already know how to calculate <with|mode|math|P(L\|E,M<rsub|I>)> and
  <with|mode|math|P(L\|E,M<rsub|=>)>, so we need to calculate
  <with|mode|math|P(M<rsub|I>\|E) >and <with|mode|math|P(M<rsub|=>\|E)>.

  <\equation*>
    P(M<rsub|I>\|E)=P(E\|M<rsub|I>)<frac|P(M<rsub|I>)|P(E)>
  </equation*>

  <\equation*>
    =P(E\|M<rsub|I>)<frac|P(M<rsub|I>)|P(E\|M<rsub|I>)P(M<rsub|I>)+P(E\|M<rsub|=>)P(M<rsub|=>)>
  </equation*>

  And similarly for <with|mode|math|P(E\|M<rsub|=>)>.

  <subsection|Calculations (continuous case)>

  In this case, we take <with|mode|math|t<rsub|k>> to mean the time spent
  searching at k, rather than the number of tests at <with|mode|math|k>;
  <with|mode|math|r<rsub|k>> as the expected number of detections at
  <with|mode|math|k> if we spend one unit of time \ searching there; and
  <with|mode|math|d<rsub|k>> as the number of detections at
  <with|mode|math|k>.

  Now,\ 

  <\with|mode|math>
    \;

    <\equation*>
      P(E\|L,r<rsub|0>\<ldots\>r<rsub|N>) =
      <choice|<tformat|<table|<row|<cell|0>|<cell|if d<rsub|k>\<neq\>0 for
      any k\<less\>L >>|<row|<cell|>|<cell|>>|<row|<cell|<big|prod><rsub|i=L\<ldots\>N>Poisson(d<rsub|i>,r<rsub|i>*t<rsub|i>)>|<cell|otherwise>>>>>
    </equation*>
  </with>

  <\equation*>
    P(E\|L,r<rsub|0>\<ldots\>r<rsub|N>) =
    <choice|<tformat|<table|<row|<cell|0>|<cell|if d<rsub|k>\<neq\>0 for any
    k\<less\>L >>|<row|<cell|>|<cell|>>|<row|<cell|<frac|e<rsup|-r<rsub|k>t<rsub|k>>(r<rsub|k>t<rsub|k>)<rsup|d<rsub|k>>|d<rsub|K>!>>|<cell|otherwise>>>>>
  </equation*>

  \;

  As before, define <with|mode|math|g(E,L)>:

  <\equation*>
    \;
  </equation*>

  <\equation*>
    g(E,L)=<big|int><rsub|r<rsub|k>=0\<ldots\>1>P(E\|L,r<rsub|k>)P(L)pdf(r<rsub|k>)
  </equation*>

  Problem: now we need a different prior on <with|mode|math|r<rsub|k>>. We
  could take this as the scale-free uninformative prior
  <with|mode|math|1/r<rsub|k>>. However, this is an improper prior.
  Alternatively, we could take a uniform prior on <with|mode|math|p<rsub|k>,
  where p<rsub|k>=Poisson(1,r<rsub|k>)=r<rsub|k>e<rsup|-r<rsub|k>>>. Hence
  <with|mode|math|-p<rsub|k>=-r<rsub|k>e<rsup|-r<rsub|k>>> and therefore
  <with|mode|math|r<rsub|k>=-W(p<rsub|k>)>
</body>

<\initial>
  <\collection>
    <associate|info-flag|short>
    <associate|language|british>
    <associate|sfactor|4>
  </collection>
</initial>

<\references>
  <\collection>
    <associate|auto-1|<tuple|1|?>>
    <associate|auto-10|<tuple|3|?>>
    <associate|auto-2|<tuple|2|?>>
    <associate|auto-3|<tuple|2.1|?>>
    <associate|auto-4|<tuple|1|?>>
    <associate|auto-5|<tuple|2.2|?>>
    <associate|auto-6|<tuple|2|?>>
    <associate|auto-7|<tuple|2.3|?>>
    <associate|auto-8|<tuple|2.4|?>>
    <associate|auto-9|<tuple|2.5|?>>
  </collection>
</references>

<\auxiliary>
  <\collection>
    <\associate|table>
      <\tuple|normal>
        \;
      </tuple|<pageref|auto-4>>

      <tuple|normal||<pageref|auto-6>>
    </associate>
    <\associate|toc>
      <with|par-left|<quote|1.5fn>|Introduction
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-1>>

      <with|par-left|<quote|1.5fn>|Calculations (discrete case)
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-2>>

      <with|par-left|<quote|3fn>|Definitions
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-3>>

      <with|par-left|<quote|3fn>|Assuming constant <with|mode|<quote|math>|r>
      at all locations <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-5>>

      <with|par-left|<quote|3fn>|Multiple <with|mode|<quote|math>|r<rsub|i>>
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-7>>

      <with|par-left|<quote|3fn>|Independent
      <with|mode|<quote|math>|r<rsub|i>> <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-8>>

      <with|par-left|<quote|3fn>|Two models for <with|mode|<quote|math>|r>
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-9>>

      <with|par-left|<quote|1.5fn>|Calculations (continuous case)
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-10>>
    </associate>
  </collection>
</auxiliary>