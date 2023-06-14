#!/usr/bin/python3
import sys,os,json,re
from PIL import Image
from PIL.ExifTags import TAGS
# import piexif
# import piexif.helper

RAW=False
# RAW=True


def print_raw(ImageData):
    if RAW:
        print("\nRaw Data:\n\n",ImageData,"\n")

def stringcontains(haystack,needle):
    return (haystack.find(needle) == True)

def ERR_NotImplented(message,ImageData):
    print_raw(ImageData)
    raise NotImplementedError(message)

def ERR_NoKnownMetaData(ImageData):
    print_raw(ImageData)
    raise Exception("No SD MetaData (that we know about) was found")



def do_png(IsNovelAI,IsInvokeAI,isInvokeAINew,isAutomatic1111,ImageData):
    # might be good to put our stuff in a dictionary and return that to the calling function
    # which can then do stuff like display it or shove it in a database with the image or a thumbnail of it
    # or somethin like that
    # Not entirely sure how brittle this code is - string parsing as brittle as html scraping
    # the data that we can extract is not put into the images under out control and there is no 'standardisation' (yet, maybe)
    # thought I was done and the discovered Automatic1111 does it differently again.
    # Be really nice if the keywords were standardised at the very least, then maybe the structure as well
    # that would be awesome!
    result=None
    # print("do_png(%s, %s, %s. %s)" % (IsNovelAI, IsInvokeAI, isInvokeAINew,isAutomatic1111))
    if IsNovelAI:
        result="NovelAi Generation Parameters:\n\n"
        print_raw(ImageData)
        result+="Prompt: %s \n\n" % (ImageData["Description"])
        comment=json.loads(ImageData["Comment"])
        result+="Negative Prompt: %s \n\n" % (comment["uc"])
        for key in comment.keys():
            if key != "uc":
                result+="%s:%s \n" % (key,comment[key])
    elif isInvokeAINew:
        result="InvokeAI (latest version) Generation Parameters :\n\n"
        print_raw(ImageData)
        rt=json.loads(ImageData["sd-metadata"])
        p=rt["image"]["prompt"]
        result+="Prompt:%s \n\n" % (p.split("[",1)[0].strip())
        # there's probably better ways to do the next bit of tidying up the strings
        n = re.findall(r'\[.*\]', p)[0]
        n = re.sub(r'[\[\]]', '', n)
        result+="Negative Prompt: %s \n\n" % (''.join(n.strip()))
        for key in rt.keys():
            if key != "image":
                result+="%s:%s \n" % (key,rt[key])
        for key in rt["image"].keys():
            if key != "prompt" :
                if key != "variations":
                    result+="%s:%s \n" % (key,rt["image"][key])
                else:
                    if len(rt["image"][key]) > 0:
                        result+="%s:%s \n" % (key,''.join(rt["image"][key]))
                    else:
                        result+="%s:%s \n" % (key,"None")

    elif IsInvokeAI:
        result="InvokeAI (older version) Generation Parameters :\n\n"
        print_raw(ImageData)
        p=ImageData["Dream"].strip()
        result+="Prompt: %s \n\n" % (p.split("[",1)[0].split("\"")[1].strip())
        # there's probably better ways to do the next bit of tidying up the strings
        n = re.findall(r'\[.*\]', p)[0]
        n = re.sub(r'[\[\]]', '', n)
        result+=("Negative Prompt: %s \n\n",n.strip())
        p=p.split("]",1)[1].split("\"")[1].strip()
        p=p.replace("-s","Steps: ")
        p=p.replace("-S","\nSeed: ")
        p=p.replace("-A","\nSampler: ")
        p=p.replace("-C","\ncfg_scale: ")
        p=p.replace("-W","\nWidth: ")
        p=p.replace("-H","\nHeight: ")
        result+="%s \n" % (p.strip())
    elif isAutomatic1111:
        result="Automatic1111 Generation Parameters :\n\n""Prompt: %s" % ImageData["parameters"]
        print_raw(ImageData)
        mdata="%s" % ImageData["parameters"].replace("Negative prompt: ","")
        mdata=mdata.split("\n")
        result+="Prompt: %s \n\n" % (mdata[0])
        result+="Negative Prompt: %s \n\n" % mdata[1]
        result+="%s \n" % mdata[2].replace(", ","\n")
        #
        # Note to me:
        # Maybe anything between a colon : and a newline \n should be enclosed in a string - then be easy to make it a dict
        #
    else:
        ERR_NoKnownMetaData(ImageData)
    return result

def do_jpg(IsNovelAI,IsInvokeAI,isInvokeAINew,isAutomatic1111,ImageData):
    print("do_jpg(%s, %s, %s, %s)" % (IsNovelAI, IsInvokeAI, isInvokeAINew ,isAutomatic1111 ))
    if IsNovelAI:
        ERR_NotImplented( "Sorry jpg.IsNovelAI parsing not yet implemented")
    elif IsInvokeAI:
        ERR_NotImplented( "Sorry jpg.IsInvokeAI parsing not yet implemented")
    elif isInvokeAINew:
        ERR_NotImplented( "Sorry jpg.isInvokeAINew parsing not yet implemented")
    elif isAutomatic1111:
        ERR_NotImplented( "Sorry jpg.isAutomatic1111 parsing not yet implemented")
    else:
        ERR_NoKnownMetaData(ImageData)

def do_webp(IsNovelAI,IsInvokeAI,isInvokeAINew,isAutomatic1111,ImageData):
    print("do_webp(%s, %s, %s, %s)" % (IsNovelAI, IsInvokeAI, isInvokeAINew ,isAutomatic1111 ))
    if IsNovelAI:
        ERR_NotImplented( "Sorry webp.IsNovelAI parsing not yet implemented")
    elif IsInvokeAI:
        ERR_NotImplented( "Sorry webp.IsInvokeAI parsing not yet implemented")
    elif isInvokeAINew:
        raise NotImplementedError( "Sorry webp.isInvokeAINew parsing not yet implemented")
    elif isAutomatic1111:
        ERR_NotImplented( "Sorry webp.isAutomatic1111 parsing not yet implemented")
    else:
        ERR_NoKnownMetaData(ImageData)

def main(filename):
    imagefile=os.path.join(os.getcwd(),filename)
    ext = os.path.splitext(filename)[1].lower()
    ImageData=""
    isNovelAI = False
    isInvokeAI = False
    isInvokeAINew = False
    isAutomatic1111=False
    try:
        i = Image.open(str(imagefile))
    except:
        raise
        sys.exit()
    print ("Processing file: ",imagefile,"\n")
    # ImageData=i.text

    if ext == ".png":
        ImageData=i.info
        isNovelAI="Software" in ImageData.keys() and ImageData["Software"]=="NovelAI"
        isInvokeAI="Dream" in ImageData.keys()
        isInvokeAINew="sd-metadata" in ImageData.keys()
        isAutomatic1111="parameters" in ImageData.keys()#should be the only key - if its there
        print(do_png(isNovelAI,isInvokeAI,isInvokeAINew,isAutomatic1111,ImageData))

    elif ext == ".jpg" or ext == ".jpeg":
        ERR_NotImplented( "Sorry jpg parsing not yet implemented")
        # isNovelAI = stringcontains(ImageData,"Software=NovelAI")
        # isInvokeAI = stringcontains(ImageData,"Dream=")
        # isInvokeAINew = stringcontains(ImageData,"InvokeAI=")
        # print(do_jpg(isNovelAI,isInvokeAI,isInvokeAINew,isAutomatic1111,ImageData))

    elif ext == ".webp":
        ERR_NotImplented( "Sorry webp parsing not yet implemented")
        # isNovelAI = stringcontains(ImageData,"Software=NovelAI")
        # isInvokeAI = stringcontains(ImageData,"Dream=")
        # isInvokeAINew = stringcontains(ImageData,"InvokeAI=")
        # print(do_webp(isNovelAI,isInvokeAI,isInvokeAINew,isAutomatic1111,ImageData))

if __name__ == '__main__':
    try:
        main(sys.argv[1])
    except KeyboardInterrupt:
        print('')
        print('Keyboard interrupt')
        sys.exit(0)
    except:
        raise
