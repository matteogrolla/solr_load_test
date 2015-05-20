Project Goal:
Generate random documents and queries to perform reasonably accurate solr load tests before real data is available.
 This way the performance impact of resource intensive search features can be analyzed in an early stage of the project


Dependencies:
to run the project you need to install
-python
-numpy
-solrpy     (https://code.google.com/p/solrpy/)


Example:
A quick example can be run on solr default collection: "collection1"
edit Example.py
    to index documents on solr
        (optional) set configuration parameters
        uncomment line
            dGen.runMP(collection_url, num_docs, start_id, num_threads, get_gen_doc())
        save script
        from command line: python Example.py

    to generate queries
         comment line for document generation
         uncomment lines starting with
            qg.gen_queries
         save script
         from command line: python Example.py
