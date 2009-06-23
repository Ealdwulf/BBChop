OGDF_DIR=/home/ealdwulf/Progs/downloaded/OGDF
OGDF_INCDIR=$(OGDF_DIR)
#OGDF_LIBDIR=$(OGDF_DIR)/_release
OGDF_LIBDIR=$(OGDF_DIR)/_debug
OGDF_LIB=libOGDF.a

INCLUDES = -I$(OGDF_INCDIR)
CFLAGS = $(INCLUDES) -g3

LDFLAGS = -L $(OGDF_LIBDIR)

OBJS = main.o

$(OBJS): %.o:  %.cc
	$(CXX) $(CFLAGS) -c $< -o $@

graph-parse: $(OBJS) 
	$(CXX) $(LDFLAGS) $(OBJS)  -lOGDF -o graph-parse

