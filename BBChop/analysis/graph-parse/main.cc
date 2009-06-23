#include <iostream>
#include "ogdf/decomposition/StaticSPQRTree.h"
#include "ogdf/decomposition/BCTree.h"
#include "ogdf/basic/GraphAttributes.h"
#include "ogdf/basic/Graph_d.h"

int main(int argc,char *argv[])
{
	
	ogdf::Graph g;
	ogdf::GraphAttributes ga(g);

	ga.initAttributes(ogdf::GraphAttributes::nodeLabel);

	ga.readGML(g,std::cin);
	//	g.writeGML(std::cout);

	ogdf::BCTree bc(g);

	ogdf::StaticSPQRTree t(g);

	std::cout << "graph nodes: " 
		  << g.numberOfNodes() 
		  << " edges: " 
		  << g.numberOfEdges()
		  << "\n";
	std::cout << "spqr tree S nodes: "
		  << t.numberOfSNodes()
		  << " P nodes: "
		  << t.numberOfPNodes()
		  << " R nodes: "
		  << t.numberOfRNodes()
		  << "\n";

	ogdf::List<ogdf::NodeElement *> rNodes = t.nodesOfType(ogdf::SPQRTree::RNode);
	while(rNodes.size()>0)
	{
		const ogdf::Skeleton &s = t.skeleton(rNodes.popFrontRet());
		const ogdf::Graph &r=s.getGraph();
		std::cout << "R node Skeleton: "
			  << r.numberOfNodes()
			  << "\n";
		ogdf::node v;
		forall_nodes(v,r) {
			ogdf::node orig=s.original(v);
			ogdf::String label=ga.labelNode(orig);
			std::cout<< label <<"\n";
		}
	}
}
