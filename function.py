from subprocess import call
from google.cloud import storage

def render(request):
    location = '/tmp/renders/'
    suffix = 'tempfile'
    filename = location + suffix + '0001.png'
    
    message = request.args.get('text', default = 'HELLO', type = str)
    blender_file = "models/outrun.blend"

    # This script changes the text, it is run inside our 3D software. 
    blender_expression = "import bpy; bpy.data.objects['Text'].data.body = '%s'" % message
    # Render 3D image
    call('blender -b %s --python-expr "%s" -o %s%s -f 1' % (blender_file, blender_expression, location, suffix), shell=True)

    # upload file to GCS
    client = storage.Client()
    bucket = client.get_bucket('acg-cloudrun-renders')
    blobname = message + '.png'
    blob = bucket.blob(blobname)
    blob.upload_from_filename(filename)

    #returns a public url
    return blob.public_url