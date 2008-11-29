<TeXmacs|1.0.6.11>

<style|article>

<\body>
  <doc-data|<doc-title|Bayesian Search and
  Debugging>|<\doc-author-data|<author-name|Ealdwulf Wuffinga>>
    \;
  </doc-author-data>>

  <section|Introduction>

  Bayesian Inference is a method of reasoning in the presence of uncertainty.
  Its applied cousin, Bayesian Decision Theory, is the use of Bayesian
  inference to make decisions which maximise one's expected utility. This
  paper examines whether Bayesian Search theory (a sub-field of the decision
  theory) is useful for debugging. It is of particular interest to find
  methods for diagnosing the cause of an intermittent (non-deterministic)
  error. The first part of this paper outlines various known debugging
  techniques which can be viewed as being kinds of search, and then provides
  an introduction to Bayesian Search Theory. The second part derives two
  Bayesian search algorithms for particular cases. These are:

  <\itemize>
    <item>An algorithm for finding the location (in execution time) or a
    fault, taking into account the cost of observations, and assuming that
    check-pointing is unavailable.

    <item>An algorithm for binary search which is robust in the case of
    false-negative observations. This can be used (eg) to locate the point in
    program history where a bug which causes <em|intermittent> faults was
    introduced.
  </itemize>

  Source code for both algorithms is available.

  Because I am writing this in my spare time, this paper is also an
  invitation to full time researchers to investigate this area, as I cannot
  guarantee that I will have time to do so myself. Therefore I also list a
  number of open questions.\ 

  \;

  \ <subsection|Debugging and search>

  Many of the activities required to debug a program can be thought of as
  search [FIXME: \ citations].\ 

  A search can be thought of as consisting of:

  <\itemize-minus>
    <item>A space to be searched. We may consider more than one co-ordinate
    system over the space.

    <item>A means of probing locations in the space. We may obtain
    information about more than the location being probed (eg, searching an
    ordered list). The information may be probabilistic.

    <item>A strategy for deciding where to probe next, based on the
    \ information we have obtained so far.
  </itemize-minus>

  \;

  \;

  This is a fairly informal model, just for the purposes of categorising the
  searches we describe next. A more rigorous, set-based way of describing
  searches may be found in <cite|OGeran>, which is an overview of search as
  used in various areas of applied mathematics.\ 

  During debugging, we may search in various kinds of spaces. Some of these
  are:

  \;

  [FIXME: figure out how to fix this damn table]

  \;

  <block|<tformat|<table|<row|<cell|Space(/Time)>|<cell|Co-ordinate
  system(s)>|<cell|Target>|<cell|Information hoped to be
  acquired>>|<row|<cell|Development history>|<cell|Program
  versions>|<cell|First version exhibiting fault>|<cell|Change that cause
  fault>>|<row|<cell|Program text>|<cell|>|<cell|>|<cell|>>|<row|<cell|Space
  of inputs>|<cell|depends on kind of input>|<cell|>|<cell|>>|<row|<cell|Duration
  of execution>|<cell|Time,control flow,data flow>|<cell|state of program at
  fault>|<cell|proximate cause of fault>>|<row|<cell|Hypothesis
  space>|<cell|>|<cell|>|<cell|>>>>>

  \;

  (It may seem a bit of a stretch to call hypothesis testing a search, but we
  shall see below that the mathematics is similar. )\ 

  \;

  [Fixme: this section is disjointed]

  \;

  A given fault can often be located in many of these spaces; the choice of
  which space to search in a particular case can greatly speed up - or slow
  down - the debugging process. As can the invention of a 'space' particular
  to the problem at hand.

  \;

  In some cases the search target can be more complicated than a single
  location. In <cite|cleve00finding>, an algorithm ('Delta Debugging') is
  described which looks for a minimal subset which provokes a fault - it can
  be used to search in any space, and has been demonstrated in at least the
  space of inputs and the space of program changes (deltas, from which it
  gets its name).

  \;

  The \ co-ordinate system for a particular space is also interesting. When
  using a debugger, one usually has to search in the 'control flow'
  co-ordinate system; but quite often one actually wants to think about the
  search as being a search of the data flow, and the control flow is a
  distraction.\ 

  [fixme - more to say here?]

  <subsection|Bayesian Search Theory>

  There are two kinds of Bayesian search, depending on the source of
  uncertainty. One is where we have a prior probability distribution over the
  target space, but the search itself is deterministic. [add examples -
  Huffman, zhigljavsky's root finding methods]. The other is where the
  uncertainty also comes from the observations. [add examples - submarines,
  Search And Rescue]

  [Stuff to put here: description of basic 'boxes' search. Iida's etymology
  of search theory]

  <section|Bayesian search for debugging>

  We give two search algorithms, with different applications. The first
  assumes reliable observations, the second, without.

  <subsection|Finnegan search>

  Suppose we are using a debugger to find the instant at which a fault
  occurs, in a deterministic program. We know it to be in the interval
  [S,S+L). To make an observation (to see whether the fault has occurs yet)
  has cost C. If we have gone too far, we must restart the program from the
  beginning. (I don't know if this problem has a name, but I call it
  'Finnegan search' after the rhyme every verse of which ends, 'So poor old
  Finnegan, had to beginagain!').

  Without loss of generality, we take the cost of a single step to be 1, and
  the cost of \ restarting the debugger to be zero (not including running the
  program back to S).

  \;

  The search strategy is simply a function f(S,L,C) which returns the number
  of steps to make before the next observation. Obviously, if C is zero f is
  always one, and if C is large, f is L/2. But what about when C is in
  between?

  \;

  The optimal solution can be defined recursively:

  \;

  <\enumerate-roman>
    <item><math|f(S,L,C) = the \ k \ s.t. E(S,L,C,k) is minimised>

    <item><math|E(S,1,C,n) =0>

    <item><with|mode|math|E(S,L,C,n) = n+C+(S+E<rsub|opt>(S,L,C)p +
    E<rsub|opt>(S+n,L-n,C)*q>

    <htab|5mm><htab|5mm>(Where <math|p=<frac|n|L>> and <math|q=1-p>)

    <item><math|E<rsub|opt>(S,L,C) =E(S,L,C,f(S,L,C) )>
  </enumerate-roman>

  \;

  <math|E(S,L,C,n)> is the expected cost of the whole search, given that the
  next observation is after <math|n> steps, and the optimal strategy is used
  subsequently.\ 

  \;

  \;

  This is impractical to use, even with dynamic programming. An approximate
  solution, which empirically [FIXME - evidence] has a cost very close to the
  optimal, is to take the number of steps which gives us the best
  <em|expected> cost/benefit ratio for this observation. The expected cost is
  the number of steps, plus C, plus the probability that we have to rerun
  from the start times the cost of doing so. The expected benefit is the
  change in entropy \ of the unknown information.\ 

  This is effectively a greedy algorithm, since it maximises immediate
  return, although it seems misleading to call an algorithm greedy, which
  maximises benefit/cost rather than just benefit - one might even call it a
  <em|prudent> algorithm.

  \;

  If the best number of steps is \<gtr\>1, it can be estimated by solving for
  <math|n> (or looking up) the equation:

  \;

  \ <math|1+<frac|S+C|L> = <frac|log(n/L)|log(1-n/L)>>\ 

  [Fixme: find derivation, or redo it]

  \;

  We take the number of steps to be 1 or <math|n>, whichever has the better
  cost/benefit ratio.

  \;

  <subsection|Binary search with false-negative observations >

  It is fairly common to want to locate the point in a program's history at
  which a bug was created. Several version-control systems provide support
  for this search, but all assume that it can be determined reliably whether
  the bug is present in a given version \ - IE, the search cannot be used in
  the presence of false-negatives, such as would be cause if the only known
  symptom of the bug is intermittent faults.

  Here we derive an algorithm which takes into account the presence of false
  negatives. It is a fairly straightforward modification of the existing
  Bayesian Search algorithms cited above, for the case of uncertain
  observations.\ 

  \;

  In the SAR and military uses of Bayesian search, an observation only tells
  you about a fixed area around the search, whereas here we assume that an
  observation anywhere after the bug was introduced may detect the bug. This
  does not present much of a problem mathematically. More awkward is the fact
  that we don't know the probability that an observation will detect the bug,
  whereas for other purposes the detection function can be measured, or
  derived from physical principles. Fortunately Bayesian inference provides a
  technique for eliminating unknown variables, called 'Marginalisation'. This
  requires that we assume a prior distribution over the unknown variable. In
  this case, we assume the the probability of detection <math|r> is uniform
  in <math|0\<ldots\>1.>

  \;

  We also assume here that the history is a total order. This may not be true
  for the case where the revision control system keeps track of where
  branches have been merged to; then history is a DAG. I seen no reason why
  this algorithm cannot be generalised to the DAG case, although doing so
  would probably be messy.

  \;

  The algorithm needs to do two things: decide where to make each
  observation, and decide when to stop. In this case, we adopt the simplest
  approach, which is to always make the observation for which the expected
  entropy of the posterior distribution is smallest, and to stop when the
  probability of the most likely location reaches some reasonable value. We
  do not claim that this results in an optimal one, only a practical one.
  When search effort is continuous, rather than discrete, minimising entropy
  often results in an optimal algorithm, but that is not the case here.
  [fixme: be less wooly]

  \;

  \;

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
  (fixme: wouldn't this drop out in the end anyway?)

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

  <subsubsection|Entropy calculation>

  Now, we need to calculate the expected entropy after the observation. For
  this we need:

  <\itemize>
    <item>The probability that the observation will detect, at each location
    (<math|><math|<with|mode|text|<with|mode|math|P(D<rsub|i>\|E)>>, >above)

    <item>For each <math|L<rsub|i>>, the entropy of the probability
    distribution <math|P(L\|E<rsub|d>)> where <math|E<rsub|d>> is the
    evidence if we have another detection at <math|i>

    <item>The same entropies, for the case when we do not detect at
    <math|L<rsub|i>>.
  </itemize>

  \ This sounds like we need <math|O(N<rsup|2>)> probabilities. However, they
  are actually made up from only <math|O(N)> likelihoods <math|g(E,L>)
  because of the following:

  <\itemize-dot>
    <item>if <math|E<rsub|a>=E<rsub|b>> execpt that some <math|d<rsub|i>> in
    <math|E<rsub|a>> is replaced by <math|d<rsub|i>+1> in <math|E<rsub|b>>,
    then <math|<rsub|>g(E<rsub|a>,L<rsub|j>)=g(E<rsub|b>,L<rsub|j>) >for all
    <math|j\<less\>i>\ 

    <item>if <math|E<rsub|a>=E<rsub|b>> execpt that some <math|t<rsub|i>> in
    <math|E<rsub|a>> is replaced by <math|t<rsub|i>+1> in <math|E<rsub|b>>,
    then <math|<rsub|>g(E<rsub|a>,L<rsub|j>)=g(E<rsub|b>,L<rsub|j>) >for all
    <math|j\<less\>i>

    <item>if <math|E<rsub|a>=E<rsub|b>> execpt that some <math|d<rsub|i>> in
    <math|E<rsub|a>> is replaced by <math|d<rsub|i>+1> in <math|E<rsub|b>>,
    and <math|d<rsub|i+1>> in <math|E<rsub|b>> is replace by
    <math|d<rsub|i+1>+1> in <math|E<rsub|a>>, \ then
    <math|<rsub|>g(E<rsub|a>,L<rsub|j>)=g(E<rsub|b>,L<rsub|j>) >for all
    <math|j\<less\>i> and j\<gtr\>i

    <item>if <math|E<rsub|a>=E<rsub|b>> execpt that some <math|t<rsub|i>> in
    <math|E<rsub|a>> is replaced by <math|t<rsub|i>+1> in <math|E<rsub|b>>,
    and <math|t<rsub|i+1>> in <math|E<rsub|b>> is replace by
    <math|t<rsub|i+1>+1> in <math|E<rsub|a>>, \ then
    <math|<rsub|>g(E<rsub|a>,L<rsub|j>)=g(E<rsub|b>,L<rsub|j>) >for all
    <math|j\<less\>i> and j\<gtr\>i
  </itemize-dot>

  For Shannon entropy, there is no obvious way to make use of this fact.
  However, Reny entropy <math|H<rsub|\<alpha\>> >has a simpler algebraic
  structure:

  <\equation*>
    H<rsub|\<alpha\>>(X)=<frac|1|1-\<alpha\>>log<left|(><big|sum><rsup|n><rsub|i=1>p<rsub|i><rsup|\<alpha\>><right|)>
  </equation*>

  In the limit as <math|\<alpha\>> tends to 1, <math|H<rsub|\<alpha\>>>
  converges to the shannon entropy. So we use the Renyi entropy instead, and
  pick an <math|\<alpha\>> close to 1 in order to approximate the Shannon
  entropy. (In fact other <math|\<alpha\>> might be better, since Renyi
  entropy originated in Search theory [check this], but I have not looked
  into this.)

  By using the Renyi entropy, we can calculate all the entropies in
  <math|O(N)> time. This is still expensive, but it is sufficient to make the
  algorithm useful when the cost of making an observation is high. As a rough
  measure, it takes my (2006 Athlon) PC 1.5 seconds to compute the decision
  when N=1000. The calculation could probably be made faster, but it will
  remain <math|O(N)> if we have to calculate the entropies and probabilities
  explicitly. So an interesting question is whether an algorithm with the
  same behavior can be devised, which does not explicitely calculate
  <math|O(N)> values.

  \;

  [add more here about the behavior of the algorithm]

  \;

  This algorithm opens the possibility of tracking down intermittent bugs in
  an automated way, by leaving a machine to test versions of a program until
  one has a sufficient probability of being where the bug was introduced.

  <section|Conclusions>

  [write some conclusions]

  <subsection|Open questions>

  <\enumerate-numeric>
    <item>Are there any other useful spaces over which to search, during
    debugging?

    <item>Can one write a program such that <em|searching in it<em|>> is
    efficient? Is this the same as, or in conflict with, or independent of,
    the program being well written in existing senses?

    <item>Questions about binary search with false-negatives:

    <\enumerate-roman>
      <item>Is maximising change-in-entropy optimal?

      <item>Can we take into account the cost of switching from one location
      to another being greater than retesting the current location?

      <item>Is there a procedure which makes its decision in less than
      <math|O(n)> time, which has the same behaviour as calculating all the
      entropies?
    </enumerate-roman>

    <item>Can Zeller's 'Delta debugging' algorithm be generalised efficiently
    to the false-negative case? A straightforward approach would require
    calculating <math|O(2<rsup|N>)> probabilities, so this is not obvious. In
    <cite|Pollock1>,<cite|Pollock2>, Pollock claims that huge numbers of
    probabilities is a generic problem with Bayesian inference, and advocates
    an alternative approach based on his 'Nomic Probabilities'.\ 
  </enumerate-numeric>

  \;

  <\bibliography|bib|plain|/home/ajb/progs/checkout/BBChop/doc/a.bib>
    <\bib-list|1>
      <bibitem*|1><label|bib-Pollock1><with|font-shape|italic|J. L. Pollock,
      Knowledge and Skepticism>, chapter Reasoning defeasibly about
      probabilities. <newblock>MIT Press, 2008.

      <bibitem*|2><label|bib-cleve00finding>Holger Cleve and Andreas Zeller.
      <newblock>Finding failure causes through automated testing.
      <newblock>In <with|font-shape|italic|Automated and Algorithmic
      Debugging>, 2000.

      <bibitem*|3><label|bib-OGeran>J.H. O'Geran, H.P. Wynn, and A.A.
      Zhigljavsky. <newblock>Search. <newblock><with|font-shape|italic|Acta
      Applicandae Mathematicae>, 1991.

      <bibitem*|4><label|bib-Pollock2>J.<nbsp>L. Pollock. <newblock>Probable
      probabilities. <newblock>Technical report, OSCAR Project, 2007.
    </bib-list>
  </bibliography>
</body>

<\initial>
  <\collection>
    <associate|language|british>
  </collection>
</initial>

<\references>
  <\collection>
    <associate|auto-1|<tuple|1|1>>
    <associate|auto-10|<tuple|2|?>>
    <associate|auto-11|<tuple|2.2.3|?>>
    <associate|auto-12|<tuple|2.2.4|?>>
    <associate|auto-13|<tuple|2.2.5|?>>
    <associate|auto-14|<tuple|3|?>>
    <associate|auto-15|<tuple|3.1|?>>
    <associate|auto-16|<tuple|4|?>>
    <associate|auto-2|<tuple|1.1|1>>
    <associate|auto-3|<tuple|1.2|2>>
    <associate|auto-4|<tuple|2|2>>
    <associate|auto-5|<tuple|2.1|2>>
    <associate|auto-6|<tuple|2.2|3>>
    <associate|auto-7|<tuple|2.2.1|3>>
    <associate|auto-8|<tuple|1|3>>
    <associate|auto-9|<tuple|2.2.2|3>>
    <associate|bib-OGeran|<tuple|3|3>>
    <associate|bib-Pollock1|<tuple|1|?>>
    <associate|bib-Pollock2|<tuple|4|?>>
    <associate|bib-cleve00finding|<tuple|2|3>>
    <associate|footnote-1|<tuple|1|?>>
    <associate|footnr-1|<tuple|1|?>>
  </collection>
</references>

<\auxiliary>
  <\collection>
    <\associate|bib>
      OGeran

      cleve00finding

      Pollock1

      Pollock2
    </associate>
    <\associate|table>
      <\tuple|normal>
        \;
      </tuple|<pageref|auto-8>>

      <tuple|normal||<pageref|auto-10>>
    </associate>
    <\associate|toc>
      <vspace*|1fn><with|font-series|<quote|bold>|math-font-series|<quote|bold>|1<space|2spc>Introduction>
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-1><vspace|0.5fn>

      <with|par-left|<quote|1.5fn>|1.1<space|2spc>Debugging and search
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-2>>

      <with|par-left|<quote|1.5fn>|1.2<space|2spc>Bayesian Search Theory
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-3>>

      <vspace*|1fn><with|font-series|<quote|bold>|math-font-series|<quote|bold>|2<space|2spc>Bayesian
      search for debugging> <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-4><vspace|0.5fn>

      <with|par-left|<quote|1.5fn>|2.1<space|2spc>Finnegan search
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-5>>

      <with|par-left|<quote|1.5fn>|2.2<space|2spc>Binary search with
      false-negative observations \ <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-6>>

      <with|par-left|<quote|3fn>|2.2.1<space|2spc>Definitions
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-7>>

      <with|par-left|<quote|3fn>|2.2.2<space|2spc>Assuming constant
      <with|mode|<quote|math>|r> at all locations
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-9>>

      <with|par-left|<quote|3fn>|2.2.3<space|2spc>Multiple
      <with|mode|<quote|math>|r<rsub|i>> <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-11>>

      <with|par-left|<quote|3fn>|2.2.4<space|2spc>Independent
      <with|mode|<quote|math>|r<rsub|i>> <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-12>>

      <with|par-left|<quote|3fn>|2.2.5<space|2spc>Entropy calculation
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-13>>

      <vspace*|1fn><with|font-series|<quote|bold>|math-font-series|<quote|bold>|3<space|2spc>Conclusions>
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-14><vspace|0.5fn>

      <with|par-left|<quote|1.5fn>|3.1<space|2spc>Open questions
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-15>>

      <vspace*|1fn><with|font-series|<quote|bold>|math-font-series|<quote|bold>|Bibliography>
      <datoms|<macro|x|<repeat|<arg|x>|<with|font-series|medium|<with|font-size|1|<space|0.2fn>.<space|0.2fn>>>>>|<htab|5mm>>
      <no-break><pageref|auto-16><vspace|0.5fn>
    </associate>
  </collection>
</auxiliary>