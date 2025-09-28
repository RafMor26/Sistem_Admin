from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.utils import timezone
from clientes.models import Cliente
from producto.models import Producto, Lote, Costo
from proveedores.models import Proveedor, ProductoProveedor
from usuarios.models import Usuario
from pedidos.models import Pedido, DetallePedido
from compras.models import OrdenCompra, DetalleOrdenCompra
from inventario.models import Bodega, Stock, Merma
from produccion.models import OrdenProduccion, Consumo

class Command(BaseCommand):
    help = "Carga datos iniciales para todas las tablas del sistema ERP y genera un archivo JSON en fixtures"

    def handle(self, *args, **kwargs):
        # Crear usuarios
        usuario1, _ = Usuario.objects.get_or_create(
            nombre="Ana Torres", email="ana.torres@example.com", telefono="991112223", contrasena="clave123"
        )
        usuario2, _ = Usuario.objects.get_or_create(
            nombre="Carlos Rivas", email="carlos.rivas@example.com", telefono="993334445", contrasena="clave456"
        )

        # Crear clientes
        cliente1, _ = Cliente.objects.get_or_create(
            nombre="Comercial Los Andes", rut="55555555-5",
            direccion="Av. Los Andes 1500", telefono="227776655", email="contacto@losandes.com"
        )
        cliente2, _ = Cliente.objects.get_or_create(
            nombre="Distribuidora Austral", rut="66666666-6",
            direccion="Ruta Sur Km 12", telefono="226664433", email="ventas@austral.cl"
        )

        # Crear productos
        producto1, _ = Producto.objects.get_or_create(nombre="Aceite Vegetal 1L", categoria="Alimentos", precioBase=1200.00)
        producto2, _ = Producto.objects.get_or_create(nombre="Detergente 500ml", categoria="Limpieza", precioBase=850.00)

        # Crear lotes
        lote1, _ = Lote.objects.get_or_create(
            fechaIngreso=timezone.make_aware(timezone.datetime(2025, 9, 15)),
            fechaVencimiento=timezone.make_aware(timezone.datetime(2026, 3, 15)),
            producto=producto1, ubicacion="Pasillo 1 - Estante A"
        )
        lote2, _ = Lote.objects.get_or_create(
            fechaIngreso=timezone.make_aware(timezone.datetime(2025, 9, 16)),
            fechaVencimiento=timezone.make_aware(timezone.datetime(2026, 4, 16)),
            producto=producto2, ubicacion="Pasillo 2 - Estante B"
        )

        # Crear costos
        Costo.objects.get_or_create(monto=1100.00, lote=lote1, producto=producto1,
                                    fechaCosto=timezone.make_aware(timezone.datetime(2025, 9, 15)))
        Costo.objects.get_or_create(monto=800.00, lote=lote2, producto=producto2,
                                    fechaCosto=timezone.make_aware(timezone.datetime(2025, 9, 16)))

        # Crear proveedores
        proveedor1, _ = Proveedor.objects.get_or_create(
            nombre="Agroindustrial Norte", rut="12121212-1",
            direccion="Camino Norte 234", telefono="224445556", email="ventas@agronorte.cl"
        )
        proveedor2, _ = Proveedor.objects.get_or_create(
            nombre="Química del Sur", rut="34343434-3",
            direccion="Parque Industrial Sur 890", telefono="229998877", email="contacto@quimicasur.cl"
        )

        # Relacionar productos con proveedores
        ProductoProveedor.objects.get_or_create(producto=producto1, proveedor=proveedor1,
                                                precio=1100.00, fechaRegistro=timezone.now())
        ProductoProveedor.objects.get_or_create(producto=producto2, proveedor=proveedor2,
                                                precio=800.00, fechaRegistro=timezone.now())

        # Crear pedidos relacionados con clientes y productos
        pedido1, _ = Pedido.objects.get_or_create(cliente=cliente1, usuario=usuario1,
                                                  fecha=timezone.make_aware(timezone.datetime(2025, 9, 17)))
        DetallePedido.objects.get_or_create(pedido=pedido1, producto=producto1, cantidad=10, precioUnitario=1200.00)

        pedido2, _ = Pedido.objects.get_or_create(cliente=cliente2, usuario=usuario2,
                                                  fecha=timezone.make_aware(timezone.datetime(2025, 9, 18)))
        DetallePedido.objects.get_or_create(pedido=pedido2, producto=producto2, cantidad=20, precioUnitario=850.00)

        # Crear órdenes de compra relacionadas con proveedores y productos
        orden_compra1, _ = OrdenCompra.objects.get_or_create(
            proveedor=proveedor1, usuario=usuario1,
            fecha=timezone.make_aware(timezone.datetime(2025, 9, 19)), estado="pendiente"
        )
        DetalleOrdenCompra.objects.get_or_create(ordenCompra=orden_compra1, producto=producto1, cantidad=50, precioUnitario=1100.00)

        orden_compra2, _ = OrdenCompra.objects.get_or_create(
            proveedor=proveedor2, usuario=usuario2,
            fecha=timezone.make_aware(timezone.datetime(2025, 9, 20)), estado="aprobada"
        )
        DetalleOrdenCompra.objects.get_or_create(ordenCompra=orden_compra2, producto=producto2, cantidad=30, precioUnitario=800.00)

        # Crear bodegas
        bodega1, _ = Bodega.objects.get_or_create(nombre="Bodega Norte", region="Región de Antofagasta",
                                                  direccion="Av. Minera 456", capacidad=2000)
        bodega2, _ = Bodega.objects.get_or_create(nombre="Bodega Sur", region="Región del Biobío",
                                                  direccion="Camino a Talcahuano 789", capacidad=1500)

        # Crear stock
        Stock.objects.get_or_create(cantidad=300, lote=lote1, bodega=bodega1)
        Stock.objects.get_or_create(cantidad=200, lote=lote2, bodega=bodega2)

        # Crear mermas
        Merma.objects.get_or_create(lote=lote1, cantidad=15, motivo="Derrame parcial")
        Merma.objects.get_or_create(lote=lote2, cantidad=10, motivo="Error en etiquetado")

        # Crear órdenes de producción
        orden_produccion1, _ = OrdenProduccion.objects.get_or_create(
            fechaInicio=timezone.make_aware(timezone.datetime(2025, 9, 21)),
            fechaFinalizacion=timezone.make_aware(timezone.datetime(2025, 9, 23)), estado="en proceso"
        )
        Consumo.objects.get_or_create(ordenProduccion=orden_produccion1, producto=producto1, cantidad=100, merma=5)

        # Generar archivo JSON en fixtures
        output_file = "fixtures/seed_catalog.json"
        with open(output_file, "w") as f:
            call_command("dumpdata", indent=2, stdout=f)

        self.stdout.write(self.style.SUCCESS(
            f"Datos iniciales cargados correctamente y archivo generado en {output_file}"
        ))
