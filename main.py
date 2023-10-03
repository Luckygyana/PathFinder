from graph import Graph
from metaphor_python import Metaphor
import networkx as nx
import matplotlib.pyplot as plt
import pydot
from networkx.drawing.nx_pydot import graphviz_layout
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, PageBreak, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import PageTemplate, BaseDocTemplate, Frame
from reportlab.platypus.flowables import PageBreak
from reportlab.platypus import Image
from reportlab.lib.pagesizes import letter

def metaphor_content(nodes, topic):

    metaphor = Metaphor("96486fae-2127-4d1c-ae51-a9a88dfd91bc") 
    link_dicts = {}
    for node in nodes:
        response = metaphor.search(
            "Learn " + node + "for" + topic,
            num_results=10,
            use_autoprompt=True,
            type="keyword",
        )
        contents_response = response.get_contents()
        
        links = []

        # Print content for each result               
        for content in contents_response.contents:
            links.append({
                "title": content.title,
                "extract": content.extract,
                "url": content.url,
            })

        link_dicts[node] = links

    return link_dicts

def create_graph_image(graph_data, topic):
    G = nx.DiGraph()

    for node, children in graph_data.items():
        G.add_node(node)
        G.add_edges_from([(node, child) for child in children])


    
    plt.figure(figsize=(100, 20))
    pos = graphviz_layout(G, prog="dot")
    nx.draw(G, pos, with_labels=True, node_size=3200, node_color='lightblue', font_size=12, font_weight='bold', edge_color='gray')


    plt.title(f"Learning Graph for {topic}")
    plt.axis('off')
  

    png_file = f"results/{topic}_graph.pdf"
    plt.savefig(png_file, format="pdf")

    return G.nodes
    
def create_resources_pdf(resource_data, descriptions, topic):
    # Create a PDF document
    doc = SimpleDocTemplate(f"results/{topic}_resources.pdf", pagesize=letter)
    story = []

    # Define styles for the document
    styles = getSampleStyleSheet()
    style_heading = styles["Heading1"]
    style_heading.alignment = 1  # Center alignment

    # Add the title page
    title = f"Learning {topic}"
    story.append(Paragraph(title, style_heading))
    story.append(Spacer(1, 12))


    # Add the table of contents
    story.append(PageBreak())
    story.append(Paragraph("Table of Contents", style_heading))
    story.append(Spacer(1, 12))

    table_data = []
    for key in descriptions.keys():
        table_data.append([Paragraph(key, styles["Normal"])])
    table = Table(table_data, colWidths=2.0 * inch, rowHeights=0.4 * inch)
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                            ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
    story.append(table)
    story.append(PageBreak())

    # Add content pages
    for key in resource_data.keys():
        story.append(Paragraph(key, style_heading))
        story.append(Paragraph(descriptions[key], styles["Normal"]))

        # Add URLs with hyperlinks
        for data in range(len(resource_data[key])):
            link = "<a href='%s' color='blue'><u>%s</u></a>" % (data['link'], data['title'])
            story.append(Paragraph(link, styles["Normal"]))

        story.append(PageBreak())

    # Build the PDF document
    doc.build(story)

if __name__ == "__main__":
    topic = input("What you want to Learn?: ")
    graph = Graph(topic)
    graph_data, descriptions = graph.generate_graph()
    nodes = create_graph_image(graph_data, topic)
    resource_data = metaphor_content(nodes, topic)
    create_resources_pdf(resource_data, descriptions, topic)
