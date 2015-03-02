import arcpy
import xml.dom.minidom as DOM
from os.path import exists, isfile, join
from os import makedirs


class Py(object):

    def __init__(self):
        super(Py, self).__init__()

        arcpy.env.overwriteOutput = True

    def create_sd_draft(self, tempFolder, connection_file, **kwargs):
        '''CreateMapSDDraft (arcpy.mapping)
        http://resources.arcgis.com/en/help/main/10.2/index.html#//00s30000006q000000

        requires:
            map_document: The path to mxd. We will turn it into an arcpy map document.
            service_name: The name of the service.
            folder_name: The name of the folder the service resides in. Defaults to `None`.

            copy_data_to_server: Defaults to `False`.
            server_type: Defaults to `ARCGIS_SERVER`
            summary: Optional summary text.
            tags: Optional tag text.

            out_sddraft: we can use the grunt local location for this.
            connection_file_path: I don't think we need this at this point. We can set it
                                  during staging.

        returns: Probably needs to return the location of the sddraft along with the dictionary
                 of junk that arcpy creates so we know where to point analyze.
        '''

        resource = kwargs['resource']
        if not resource or not exists(resource) or not isfile(resource):
            raise Exception('Could not find resource {}'.format(resource))

        map_document = arcpy.mapping.MapDocument(resource)
        service_name = kwargs['serviceName']
        out_sddraft = join(tempFolder, 'draft.sddraft')
        folder = ''

        if 'folder' in kwargs:
            folder = kwargs['folder']

        results = arcpy.mapping.CreateMapSDDraft(map_document,
                                                 out_sddraft,
                                                 service_name,
                                                 'ARCGIS_SERVER',
                                                 connection_file,
                                                 folder_name=folder)

        if results['errors'] == {}:
            return out_sddraft
        else:
            raise Exception(results['errors'])

    def analyze_sd(self, sddraft_path):
        '''AnalyzeForSD (arcpy.mapping)
        http://resources.arcgis.com/en/help/main/10.2/index.html#//00s30000006p000000

        requires:
            sddraft: The path to the `.sddraft` file.

        returns: Returns the junk dictionary of errors warnings and messages.
                 Do we want to format those and raise on error and let the others just print?
        '''

        print('Analyzing the sd draft. {}'.format(sddraft_path))

        if not sddraft_path or not exists(sddraft_path) or not isfile(sddraft_path):
            raise Exception('Could not find the sddraft {}'.format(sddraft_path))

        return arcpy.mapping.AnalyzeForSD(sddraft_path)

    def stage_service(self, sddraft_path):
        '''Stage Service (Server)
        http://resources.arcgis.com/en/help/main/10.2/index.html#//00540000001r000000

        requires:
            in_service_definition_draft: The `.sddraft` that is created by `create_sd_draft`.
                                         This is in the temp grunt location
            out_service_definition: The spot to save the `.sd` file. Could probably use grunt local
                                    save spot for this also.
        '''

        sd_path = sddraft_path.replace('.sddraft', '.sd')

        if not sddraft_path or not exists(sddraft_path) or not isfile(sddraft_path):
            raise Exception('Could not find the sddraft {}'.format(sddraft_path))

        return arcpy.StageService_server(sddraft_path, sd_path)

    def upload_service(self, sd_path, server_connection):
        '''Upload Service Definition (Server)
        http://resources.arcgis.com/en/help/main/10.2/index.html#//00540000001p000000

        requires:
            in_sd_file: The `.sd` file created by `stage_service`.
            username: The admin username.
            password: The admin password.
            server: The server information.

            in_startupType: Whether the service should be started. Defaults to `STARTED`.

            in_server: Here we need the server info and admin credentials to create the `.ags` file.
        '''

        arcpy.UploadServiceDefinition_server(sd_path, server_connection)

    def get_server_connection_file(self, server, tempFolder):
        '''Greate GIS Server Connection File (Server)
        http://resources.arcgis.com/en/help/main/10.2/index.html#//00s300000079000000

        requires:
            server: models.Server object

        returns: path to the connection file
        '''

        fileName = 'server_connection.ags'
        fullPath = join(tempFolder, fileName)

        if not exists(tempFolder):
            makedirs(tempFolder)

        arcpy.mapping.CreateGISServerConnectionFile('ADMINISTER_GIS_SERVICES',
                                                    tempFolder,
                                                    fileName,
                                                    server.get_admin_url(),
                                                    'ARCGIS_SERVER',
                                                    username=server.username,
                                                    password=server.password)

        return fullPath

    def modify_sd_for_replacement(self, sddraft_path):
        newType = 'esriServiceDefinitionType_Replacement'
        xml = sddraft_path
        doc = DOM.parse(xml)
        descriptions = doc.getElementsByTagName('Type')
        for desc in descriptions:
            if desc.parentNode.tagName == 'SVCManifest':
                if desc.hasChildNodes():
                    desc.firstChild.data = newType
        outXml = xml
        f = open(outXml, 'w')
        doc.writexml(f)
        f.close()
