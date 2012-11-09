# TODO: Move this out of Iris


from owslib.wms import WebMapService


def _ensure_string_array(value):
    if value is None:
        result = None
    elif isinstance(value, basestring):
        result = [value]
    else:
        if not isinstance(value[0], basestring):
            raise ValueError("Not a string array")
        result = value
    return result


def filter_passes(filter, label):
    """See if any of the filters match the label."""
    filter = filter or []
    label = (label or "").lower()

    result = True
    for f in filter:
        if f.startswith("-"):
            result = f[1:].lower() not in label
        else:
            result = f.lower() in label

        if not result:
            break
        
    return result


class _WmsLayerSummary(object):
    """Describes an interrogated WMS server's layer."""
    def __init__(self, label, title, styles):
        self.label = label
        self.title = title
        self.styles = styles
        self.projections = {}

    def __str__(self):
        result = "Layer: {0}\n  Title: {1}" \
                "\n  Styles: {2}\n  Projections ({3}):" \
                .format(self.label, self.title, 
                        ", ".join(self.styles), len(self.projections))
        # Some servers have many thousands of projections per layer
        if len(self.projections) > 10:
            result += "(omitted)"
        else:
            result += ", ".join(self.projections.keys())

        return result
             
    def verbose(self, outfile, proj_filter=None, attr_filter=None):
        """Return a textual description of the layer, including attributes."""
        proj_filter = _ensure_string_array(proj_filter)
        attr_filter = _ensure_string_array(attr_filter)

        outfile.write("\nLayer: {0}\n  Title: {1}"
                      "\n  Styles: {2}\n  Projections ({3}):"
                      .format(self.label, self.title, 
                             ", ".join(self.styles), len(self.projections)))
        # Add projection strings
        for proj_name, proj_attrs in self.projections.items():
            if not filter_passes(proj_filter, proj_name):
                continue

            outfile.write("\n    '{0}' :".format(proj_name))
            # Add attribute strings
            for attr_name, attr_value in proj_attrs.items():
                # Filter attribute names
                if not filter_passes(attr_filter, attr_name):
                    continue
                if attr_name.startswith("__"):
                    continue
            
                outfile.write(" {0} = '{1}'".format(attr_name, attr_value))
                

class WmsSummary(object):
    """Describes an interrogated WMS server. Used for WMS disovery."""
    def __init__(self, server_name, title):
        """Constructs the WMS summary object. Called by :func:`wms_interrogate`.""" 
        self.server_name = server_name
        self.title = title
        self.layers = []
        
    def __str__(self, verbose=False):
        return "Summary of WMS server {0}\nTitle: {1}" \
                "\nLayers ({2}): {3}".format(self.server_name,
                     self.title, len(self.layers),
                     "".join(["\n" + str(layer) for layer in self.layers]))

    def verbose(self, outfile=None,
                       layer_filter=None,
                       proj_filter=None,
                       attr_filter=None):
        """
        Produce a fully detailed description string, including layer attributes.

        .. TIP::

            The resulting string is sometimes too big to fit in memory.
            For example, using this routine on OpenGeo.org produces a 12GB string!
            In such cases, please use the outfile keyword and/or the various filter keywords.

        Keyword arguments can be used for a case-insensitive filter of the results.
        Any filter stating with a "-" only passes if the token is not found. 

        Kwargs:
        
            * outfile      - Use this to write directly to an open file.
                             No string will be returned in this case.
            * layer_filter - Only report on layer names containing this string(s). 
            * proj_filter  - Only report on layer projection names containing this string(s).
            * attr_filter  - Only report on projection attribute names containing this string(s).

        Returns:
        
            The description string, or None if outfile was provided.
            
        Example::

            # Interrogate OpenGeo.org
            server = "http://demo.opengeo.org/geoserver/ows?SERVICE=WMS&"
            wms_summary = wms_interrogate(server)
            
            # Print a normal summary (no projection attributes)
            print wms_summary

            # Print all layers, with only this projection and it's box attributes
            print wms_summary.verbose(proj_filter="4326", attr_filter="box") 

            # Write all layers and projections with only these projection attributes
            with open("custom_summary.txt", "wt") as outfile:
                outfile.write(wms_summary.verbose(attr_filter=["-crsoptions", "-timepositions"])) 
       
        """
        layer_filter = _ensure_string_array(layer_filter)
        
        # If we're returning a string, create a "string file" to write to.
        if outfile is None:
            outfile = StringIO.StringIO() 
        
        outfile.write("Summary of WMS server: {0}\nTitle: {1}" 
                      "\nLayers ({2}):".format(self.server_name,
                                               self.title, len(self.layers)))
        # Add layer strings
        for layer in self.layers:
            # filter layer names
            if not filter_passes(layer_filter, layer.label):
                continue
            layer.verbose(outfile, proj_filter, attr_filter)
        
        # Did we make a string file to write to?
        if isinstance(outfile, StringIO.StringIO):
            result = outfile.getvalue()
            outfile.close()
        else:
            # Written to file instead.
            result = None
            
        return result


def wms_interrogate(server_name):
    """
    Find what WMS options exist for a given WMS server.
    
    The user must be able to construct a WMS request from this information.
    
    Args:
    
        * server - WMS server url
        
    Returns:
    
        a :class:`WmsInfo` object containing the interrogation results. 
    
    Example ::
    
        server = "http://wms.jpl.nasa.gov/wms.cgi"
        wms_info = wms_interrogate(server)
        print wms_info
    
    The results can also be printed with all the layer projection attributes ::
    
        print wms_info.verbose()
        
    .. TIP:
    
        Please see the documentation for :func:`WmsSummary.verbose`
        for potentially important information regarding verbose output.
    
    """
    
    result = None
    
    # Get the service.
    wms = WebMapService(server_name)
    if "WMS" in wms.identification.type:
        result = WmsSummary(server_name, wms.identification.title)
        
        # Get every layer.
        for layer_label, layer in wms.contents.items():
            result.layers.append(_WmsLayerSummary(layer_label, layer.title, layer.styles.keys()))

            # Get every projection for this layer.
            for crs in layer.crsOptions:

                # Get attributes of the projection
                result.layers[-1].projections[crs] = attrs = {} 
                for attr_name in dir(layer):
                    if attr_name.startswith("__"):
                        continue
                    if attr_name in ["name", "parent"]:
                        continue
                    attrs[attr_name] = getattr(layer, attr_name)
    else:
        return "Unhandled type: {}".format(wms.identification.type)
                    
    return result


if __name__ == "__main__":

    print "\n-------------------------\n"
    
#    # nasa, no longer delivering full wms
#    server = "http://wms.jpl.nasa.gov/wms.cgi"
    
#    # osm uk - duplicate layer crashes owslib
#    server = "http://www.osmgb.org.uk/ogc/wms?version=1.1.1"
    
#    # eea (not particularly pertinent content)
#    server = "http://discomap-test.eea.europa.eu/ArcGIS/services/Land/CLC2000_Cach_WM/MapServer/WMSServer"
    

#    # Interrogate EEA server.
#    server = "http://discomap-test.eea.europa.eu/ArcGIS/services/Land/CLC2000_Cach_WM/MapServer/WMSServer"
#    wms_summary = wms_interrogate(server)
#
#    # Print a normal summary (no projection attributes).
#    print wms_summary
#
#    # Print a verbose summary.
#    print wms_summary.verbose()

    
#    # Interrogate OpenGeo.org.
#    server = "http://demo.opengeo.org/geoserver/ows?SERVICE=WMS&"
#    wms_summary = wms_interrogate(server)
#    
#    # Don't print an unfiltered verbose summary it's a 12GB string.
#    # print wms_summary.verbose()
#
#    # Write all layers and projections, with only bounding box attributes
#    with open("custom_summary.txt", "wt") as outfile:
#        outfile.write(wms_summary.verbose(proj_filter="4326", attr_filter="box")) 
#
#    # Print one layer and projection, without certain attributes
#    print wms_summary.verbose(layer_filter="naturalearth",
#                              proj_filter="4326",
#                              attr_filter=["-crsoptions", "-timepositions"]) 


    # Historical wms - forbidden (from work, anyhoo)
    #server = "http://www.histosm.org/"


    # WORLD OSM WMS
    server = "http://129.206.228.72/cached/osm?"
    
    print server
    print "interrogating server",
    import time
    start_time = time.time()
    wms_summary = wms_interrogate(server)
    print " ({0:.2f}s)".format(time.time() - start_time)
    
    print wms_summary
    print "\n-------------------------\n"




    # John Mooney's test wms server
    server = "http://exxvmgpmdev0.meto.gov.uk:8399/arcgis/services/JM_test/DMMS_test_global/MapServer/WMSServer"
    
    print server
    print "interrogating server",
    import time
    start_time = time.time()
    wms_summary = wms_interrogate(server)
    print " ({0:.2f}s)".format(time.time() - start_time)
    
    print wms_summary
    print "\n-------------------------\n"


