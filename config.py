import logging

class JobConfig():
    EXTRACTION_URL='http://extractionsvc:9891/extract_content'
    INFERENCE_URL='http://classifiersvc:9891/infer_content'
    SAVE_URL='http://savesvc:9891/savecontent'    
    LOGGINGLEVEL=logging.DEBUG
