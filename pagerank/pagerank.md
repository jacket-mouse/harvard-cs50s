# pagerank

一个写代码时疏漏的点：递归式求解时，注意p和i的关系，是i可以到达p，但p不一定能到达i，在写代码时把这俩的关系弄反了，导致排查了很久的Bug。