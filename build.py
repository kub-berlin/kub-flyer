import sys

from weasyprint import HTML


HTML(sys.argv[1]).write_pdf(sys.argv[2])
