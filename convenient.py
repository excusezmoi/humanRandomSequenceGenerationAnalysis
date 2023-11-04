def getNestedAttr(obj, attrStr): #attrStr: ".attr1.attr2.attr3..."
    attrGen = (attr for attr in attrStr.split(".") if attr)
    
    def recurAttr(obj, attrGen):
        try:
            obj = getattr(obj, next(attrGen))
            return recurAttr(obj, attrGen)
        except:
            return obj
        
    return recurAttr(obj, attrGen)