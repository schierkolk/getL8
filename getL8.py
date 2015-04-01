#pathrow from S3 L* Bucket List
#Output Directory

import sys, getopt
import boto
#from boto.s3.connection import S3Connection
import os

AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY =''

def main(argv):
    pathrow = ''
    output = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:b:",["ipathrow=","ofile=","bands"])
    except getopt.GetoptError:
        print 'getL8.py -p <pathrow> -o <outputpath> , -b <bands> 1,2,3'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'getL8.py -i <pathrow> -o <outputpath> -b <bands> 1,2,3'
            sys.exit(1)
        elif opt in ("-i", "--ifile"):
            pathrow = arg
        elif opt in ("-o", "--ofile"):
            output = arg
        elif opt in ("-b", "--bands"):
            rbands = arg
    #print 'Pathrow: ', pathrow
    #print 'Output: ', output

    try:
    #pathname = parsename('LC80030172015001LGN00')
        pathname = parsename(pathrow)
        #conn = S3Connection(AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY)
        conn = boto.connect_s3(AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY)
        bucket = conn.get_bucket('landsat-pds')
        #key = bucket.get_key('L8/003/017/LC80030172015001LGN00/LC80030172015001LGN00_B1.TIF')

        #key.get_contents_to_filename('LC80030172015001LGN00_B1.TIF')
        #for num in range(1,9):
        for num in rbands.split(","):
            pathnamefile = pathname + "_B" + str(num) + '.TIF'
            #print pathnamefile
            filename = output.replace("'\'","/") + "/" + os.path.basename(pathnamefile)
            key = bucket.get_key(pathnamefile)
            key.get_contents_to_filename(filename)
    except:
        sys.exit(1)

def parsename(name):
    #Build Path for S3 Download
    try:
        path = str(name[3:6])
        row = str(name[6:9])
        return 'L8/' + path + "/" + row + "/" + name + "/" + name
    except:
        sys.exit(1)

if __name__ == "__main__":

        main(sys.argv[1:])
