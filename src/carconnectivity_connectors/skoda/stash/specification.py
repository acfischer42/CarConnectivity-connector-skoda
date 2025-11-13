"""Module for vehicle specification classes."""
from __future__ import annotations
from typing import TYPE_CHECKING

from carconnectivity.objects import GenericObject
from carconnectivity.attributes import StringAttribute, DateAttribute, LevelAttribute, EnumAttribute
from carconnectivity.vehicle import GenericVehicle

if TYPE_CHECKING:
    from typing import Optional
    from carconnectivity.objects import GenericObject as GenericObjectType


class Engine(GenericObject):
    """
    Represents the engine details of a Skoda vehicle.
    
    Attributes:
        type (StringAttribute): Engine fuel type (e.g., "TDI", "TSI", "TFSI")
        powerInKW (StringAttribute): Engine power in kilowatts
        capacityInLiters (StringAttribute): Engine displacement in liters
    """

    def __init__(self, parent: Optional[GenericObjectType] = None, origin: Optional[Engine] = None) -> None:
        if origin is not None:
            super().__init__(object_id='engine', parent=parent, origin=origin)
            # Preserve all attributes from origin with safe copying
            self._copy_attribute_from_origin(origin, 'type')
            self._copy_attribute_from_origin(origin, 'powerInKW')
            self._copy_attribute_from_origin(origin, 'capacityInLiters')
        else:
            super().__init__(object_id='engine', parent=parent)
            # Engine fields matching the JSON structure
            self.type = StringAttribute(name='type', parent=self, tags={'connector_custom'})
            self.powerInKW = StringAttribute(name='powerInKW', parent=self, tags={'connector_custom'})
            self.capacityInLiters = StringAttribute(name='capacityInLiters', parent=self, tags={'connector_custom'})
    
    def _copy_attribute_from_origin(self, origin: Engine, attr_name: str) -> None:
        """Safely copy an attribute from origin object."""
        if hasattr(origin, attr_name):
            source_attr = getattr(origin, attr_name)
            setattr(self, attr_name, source_attr)
            if hasattr(source_attr, 'parent'):
                source_attr.parent = self


class ExteriorDimensions(GenericObject):
    """
    Represents the exterior dimensions of a Skoda vehicle.
    
    Attributes:
        lengthInMm (StringAttribute): Vehicle length in millimeters
        widthInMm (StringAttribute): Vehicle width in millimeters  
        heightInMm (StringAttribute): Vehicle height in millimeters
    """

    def __init__(self, parent: Optional[GenericObjectType] = None, origin: Optional[ExteriorDimensions] = None) -> None:
        if origin is not None:
            super().__init__(object_id='exteriorDimensions', parent=parent, origin=origin)
            # Preserve all attributes from origin with safe copying
            self._copy_attribute_from_origin(origin, 'lengthInMm')
            self._copy_attribute_from_origin(origin, 'widthInMm')
            self._copy_attribute_from_origin(origin, 'heightInMm')
        else:
            super().__init__(object_id='exteriorDimensions', parent=parent)
            # Exterior dimensions fields matching the JSON structure
            self.lengthInMm = StringAttribute(name='lengthInMm', parent=self, tags={'connector_custom'})
            self.widthInMm = StringAttribute(name='widthInMm', parent=self, tags={'connector_custom'})
            self.heightInMm = StringAttribute(name='heightInMm', parent=self, tags={'connector_custom'})
    
    def _copy_attribute_from_origin(self, origin: ExteriorDimensions, attr_name: str) -> None:
        """Safely copy an attribute from origin object."""
        if hasattr(origin, attr_name):
            source_attr = getattr(origin, attr_name)
            setattr(self, attr_name, source_attr)
            if hasattr(source_attr, 'parent'):
                source_attr.parent = self


class Gearbox(GenericObject):
    """
    Represents the gearbox details of a Skoda vehicle.
    
    Attributes:
        type (StringAttribute): Gearbox type identifier (e.g., "A7F", "M6F")
    """

    def __init__(self, parent: Optional[GenericObjectType] = None, origin: Optional[Gearbox] = None) -> None:
        if origin is not None:
            super().__init__(object_id='gearbox', parent=parent, origin=origin)
            # Preserve all attributes from origin with safe copying
            self._copy_attribute_from_origin(origin, 'type')
        else:
            super().__init__(object_id='gearbox', parent=parent)
            # Gearbox fields matching the JSON structure
            self.type = StringAttribute(name='type', parent=self, tags={'connector_custom'})
    
    def _copy_attribute_from_origin(self, origin: Gearbox, attr_name: str) -> None:
        """Safely copy an attribute from origin object."""
        if hasattr(origin, attr_name):
            source_attr = getattr(origin, attr_name)
            setattr(self, attr_name, source_attr)
            if hasattr(source_attr, 'parent'):
                source_attr.parent = self


class Specification(GenericObject):
    """
    Represents the complete specification details of a Skoda vehicle.
    
    This class provides a structured representation of vehicle specifications
    that mirrors the Skoda API JSON response format, with nested objects for
    complex data like engine details, exterior dimensions, and gearbox information.
    
    Attributes:
        title (StringAttribute): Full vehicle title (e.g., "Škoda Octavia Combi")
        manufacturing_date (DateAttribute): Vehicle manufacturing date
        model_year (StringAttribute): Model year as string
        body (StringAttribute): Body type (e.g., "Combi", "Sedan")
        trim_level (StringAttribute): Trim level (e.g., "Sportline", "Style")
        exterior_colour (StringAttribute): Exterior color description
        system_code (StringAttribute): Internal system code
        system_model_id (StringAttribute): System model identifier
        
        exteriorDimensions (ExteriorDimensions): Nested exterior dimensions object
        engine (Engine): Nested engine details object  
        gearbox (Gearbox): Nested gearbox details object
    """

    def __init__(self, parent: Optional[GenericObjectType] = None, origin: Optional[Specification] = None) -> None:
        if origin is not None:
            super().__init__(object_id='specification', parent=parent, origin=origin)
            
            # Copy basic attributes from origin with safe copying
            self._copy_attribute_from_origin(origin, 'title')
            self._copy_attribute_from_origin(origin, 'manufacturing_date') 
            self._copy_attribute_from_origin(origin, 'trim_level')
            self._copy_attribute_from_origin(origin, 'system_code')
            self._copy_attribute_from_origin(origin, 'system_model_id')
            self._copy_attribute_from_origin(origin, 'body')
            self._copy_attribute_from_origin(origin, 'exterior_colour')
            self._copy_attribute_from_origin(origin, 'model_year')
            self._copy_attribute_from_origin(origin, 'steering_wheel_position')
            
            # Copy nested objects with proper origin handling
            self._copy_nested_object_from_origin(origin, 'exteriorDimensions', ExteriorDimensions)
            self._copy_nested_object_from_origin(origin, 'engine', Engine) 
            self._copy_nested_object_from_origin(origin, 'gearbox', Gearbox)
        else:
            super().__init__(object_id='specification', parent=parent)
            self._initialize_attributes()
    
    def _initialize_attributes(self) -> None:
        """Initialize all specification attributes."""
        # Basic specification fields
        self.title = StringAttribute(name='title', parent=self, tags={'connector_custom'})
        self.manufacturing_date = DateAttribute(name='manufacturing_date', parent=self, tags={'connector_custom'})
        self.trim_level = StringAttribute(name='trim_level', parent=self, tags={'connector_custom'})
        self.system_code = StringAttribute(name='system_code', parent=self, tags={'connector_custom'})
        self.system_model_id = StringAttribute(name='system_model_id', parent=self, tags={'connector_custom'})
        self.body = StringAttribute(name='body', parent=self, tags={'connector_custom'})
        self.exterior_colour = StringAttribute(name='exterior_colour', parent=self, tags={'connector_custom'})
        self.model_year = StringAttribute(name='model_year', parent=self, tags={'connector_custom'})
        
        # Steering wheel position from air conditioning API
        self.steering_wheel_position = EnumAttribute(
            name='steering_wheel_position', 
            parent=self, 
            value_type=GenericVehicle.VehicleSpecification.SteeringPosition,
            tags={'connector_custom'}
        )
        
        # Nested objects matching JSON structure
        self.exteriorDimensions = ExteriorDimensions(parent=self)
        self.engine = Engine(parent=self)
        self.gearbox = Gearbox(parent=self)
    
    def _copy_attribute_from_origin(self, origin: Specification, attr_name: str) -> None:
        """Safely copy an attribute from origin object."""
        if hasattr(origin, attr_name):
            source_attr = getattr(origin, attr_name)
            setattr(self, attr_name, source_attr)
            if hasattr(source_attr, 'parent'):
                source_attr.parent = self
    
    def _copy_nested_object_from_origin(self, origin: Specification, attr_name: str, object_class) -> None:
        """Safely copy a nested object from origin with proper type handling."""
        if hasattr(origin, attr_name):
            origin_nested = getattr(origin, attr_name)
            setattr(self, attr_name, object_class(parent=self, origin=origin_nested))
        else:
            # Create empty nested object if not in origin
            setattr(self, attr_name, object_class(parent=self))
