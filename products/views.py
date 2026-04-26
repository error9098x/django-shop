from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import html

# Fixed: SQL Injection using parameterized query
def search_products(request):
    query = request.GET.get('q', '')
    sql = "SELECT * FROM products WHERE name LIKE %s"
    
    with connection.cursor() as cursor:
        cursor.execute(sql, [f"%{query}%"])
        results = cursor.fetchall()
    
    return render(request, 'products/search_results.html', {'results': results})

# Fixed: XSS - using Django template rendering with auto-escaping
def product_detail(request, product_id):
    product_name = request.GET.get('name', '')
    return render(request, 'products/product_detail.html', {'product_name': product_name})

# Fixed: Removed csrf_exempt, using parameterized query
def update_order(request, order_id):
    if request.method == 'POST':
        status = request.POST.get('status')
        sql = "UPDATE orders SET status = %s WHERE id = %s"
        
        with connection.cursor() as cursor:
            cursor.execute(sql, [status, order_id])
        
        return HttpResponse("Order updated")
    return HttpResponse("Invalid request")

# Fixed: Path traversal - validate and sanitize file path
import os
from django.conf import settings

def download_invoice(request):
    filename = request.GET.get('file', '')
    # Sanitize filename to prevent path traversal
    filename = os.path.basename(filename)
    filepath = os.path.join(settings.BASE_DIR, 'invoices', filename)
    filepath = os.path.abspath(filepath)
    
    # Ensure the resolved path is within the allowed directory
    allowed_dir = os.path.abspath(os.path.join(settings.BASE_DIR, 'invoices'))
    if not filepath.startswith(allowed_dir):
        return HttpResponse("Invalid file path", status=400)
    
    try:
        with open(filepath, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        return HttpResponse("File not found", status=404)
    
    return HttpResponse(content, content_type='text/plain')
