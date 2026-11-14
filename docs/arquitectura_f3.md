# Arquitectura del núcleo de F3

## Diagrama de clases

```mermaid
classDiagram
    direction TB

    class EtapaBase {
        <<abstracta>>
        +ejecutar(datos) DataFrame*
    }

    class Pipeline {
        -tuple _etapas
        +etapas tuple
        +ejecutar(datos) DataFrame
    }

    class FiltroColelitiasis {
        +ejecutar(datos) DataFrame
    }

    class AsignadorProvincia {
        +ejecutar(datos) DataFrame
    }

    class MarcadorGruposRiesgo {
        +ejecutar(datos) DataFrame
    }

    class MarcadorColecistectomia {
        +ejecutar(datos) DataFrame
    }

    EtapaBase <|-- FiltroColelitiasis
    EtapaBase <|-- AsignadorProvincia
    EtapaBase <|-- MarcadorGruposRiesgo
    EtapaBase <|-- MarcadorColecistectomia
    Pipeline o-- "1..*" EtapaBase : contiene
```

## Cómo leer el diagrama

- **Herencia:** las cuatro clases de etapa heredan de `EtapaBase`, lo que las obliga a implementar el método `ejecutar`.
- **Polimorfismo:** el `Pipeline` llama a `ejecutar` en cada etapa sin necesitar saber cuál es; cada una responde a su propia manera.
- **Encapsulamiento:** el `Pipeline` guarda sus etapas en el atributo interno `_etapas` y solo permite consultarlas mediante la propiedad `etapas`, no modificarlas.
- **Patrón de diseño:** se aplica el patrón *Pipeline* (tubería). Cada etapa recibe la tabla, la transforma y la entrega a la siguiente. Para agregar un paso nuevo basta con crear otra clase que herede de `EtapaBase`, sin modificar las existentes.
- 