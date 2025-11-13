"""Module for vehicle classes."""
from __future__ import annotations
from typing import TYPE_CHECKING

from carconnectivity.vehicle import GenericVehicle, ElectricVehicle, CombustionVehicle, HybridVehicle
from carconnectivity.charging import Charging
from carconnectivity.attributes import BooleanAttribute
from carconnectivity.attributes import StringAttribute
from carconnectivity.attributes import DateAttribute, LevelAttribute

from carconnectivity_connectors.skoda.capability import Capabilities
from carconnectivity_connectors.skoda.charging import SkodaCharging
from carconnectivity_connectors.skoda.climatization import SkodaClimatization
from carconnectivity_connectors.skoda.specification import Specification
from carconnectivity_connectors.skoda.service_partner import ServicePartner

SUPPORT_IMAGES = False
try:
    from PIL import Image
    SUPPORT_IMAGES = True
except ImportError:
    pass

if TYPE_CHECKING:
    from typing import Optional, Dict
    from carconnectivity.garage import Garage
    from carconnectivity_connectors.base.connector import BaseConnector


class SkodaVehicle(GenericVehicle):  # pylint: disable=too-many-instance-attributes
    """
    A class to represent a generic Skoda vehicle.
    """
    def __init__(self, vin: Optional[str] = None, garage: Optional[Garage] = None, managing_connector: Optional[BaseConnector] = None,
                 origin: Optional[SkodaVehicle] = None) -> None:
        if origin is not None:
            super().__init__(garage=garage, origin=origin)
            self.capabilities: Capabilities = origin.capabilities
            self.capabilities.parent = self
            self.in_motion: BooleanAttribute = origin.in_motion
            self.in_motion.parent = self
            # preserve raw_api and extras when copying from origin
            if hasattr(origin, 'raw_api'):
                self.raw_api = origin.raw_api
                self.raw_api.parent = self
            if hasattr(origin, 'extras'):
                self.extras = origin.extras
                self.extras.parent = self
            # preserve additional Skoda-specific attributes when copying
            if hasattr(origin, 'title'):
                self.title = origin.title
                self.title.parent = self
            if hasattr(origin, 'system_model_id'):
                self.system_model_id = origin.system_model_id
                self.system_model_id.parent = self
            if hasattr(origin, 'priority'):
                self.priority = origin.priority
                self.priority.parent = self
            if hasattr(origin, 'device_platform'):
                self.device_platform = origin.device_platform
                self.device_platform.parent = self
            if hasattr(origin, 'skoda_state'):
                self.skoda_state = origin.skoda_state
                self.skoda_state.parent = self
            if hasattr(origin, 'workshop_mode_enabled'):
                self.workshop_mode_enabled = origin.workshop_mode_enabled
                self.workshop_mode_enabled.parent = self
            if hasattr(origin, 'service_partner'):
                self.service_partner = origin.service_partner
                self.service_partner.parent = self
            if hasattr(origin, 'renders'):
                self.renders = origin.renders
                self.renders.parent = self
            if hasattr(origin, 'composite_renders'):
                self.composite_renders = origin.composite_renders
                self.composite_renders.parent = self
            if hasattr(origin, 'composite_render_urls'):
                self.composite_render_urls = origin.composite_render_urls
                self.composite_render_urls.parent = self
            # specification related
            if hasattr(origin, 'specification'):
                self.specification = Specification(parent=self, origin=origin.specification)
            else:
                self.specification = Specification(parent=self)
                if hasattr(origin, 'spec_engine_fuel_type'):
                    self.specification.engine_fuel_type = origin.spec_engine_fuel_type
                    self.specification.engine_fuel_type.parent = self.specification
                if hasattr(origin, 'spec_exterior_colour'):
                    self.specification.exterior_colour = origin.spec_exterior_colour
                    self.specification.exterior_colour.parent = self.specification
                if hasattr(origin, 'spec_model_year'):
                    self.specification.model_year = origin.spec_model_year
                    self.specification.model_year.parent = self.specification
            if SUPPORT_IMAGES:
                self._car_images = origin._car_images

        else:
            super().__init__(vin=vin, garage=garage, managing_connector=managing_connector)
            self.climatization = SkodaClimatization(vehicle=self, origin=self.climatization)
            self.capabilities = Capabilities(vehicle=self)
            self.in_motion = BooleanAttribute(name='in_motion', parent=self, tags={'connector_custom'})
            # Raw API dump for debugging / exposing unexpected keys
            self.raw_api = StringAttribute(name='raw_api', parent=self, tags={'connector_custom'})
            # Extras: aggregated unexpected or additional fields from API (JSON mapping)
            self.extras = StringAttribute(name='extras', parent=self, tags={'connector_custom'})
            self.renders = StringAttribute(name='renders', parent=self, tags={'connector_custom'})
            self.composite_renders = StringAttribute(name='composite_renders', parent=self, tags={'connector_custom'})
            self.composite_render_urls = StringAttribute(name='composite_render_urls', parent=self, tags={'connector_custom'})
            # Skoda-specific fields surfaced from API
            self.title = StringAttribute(name='title', parent=self, tags={'connector_custom'})
            self.system_model_id = StringAttribute(name='system_model_id', parent=self, tags={'connector_custom'})
            self.priority = StringAttribute(name='priority', parent=self, tags={'connector_custom'})
            self.device_platform = StringAttribute(name='device_platform', parent=self, tags={'connector_custom'})
            self.skoda_state = StringAttribute(name='skoda_state', parent=self, tags={'connector_custom'})
            self.workshop_mode_enabled = BooleanAttribute(name='workshop_mode_enabled', parent=self, tags={'connector_custom'})
            self.service_partner = ServicePartner(parent=self)
            # Specification related fields
            self.specification = Specification(parent=self)
            if SUPPORT_IMAGES:
                self._car_images: Dict[str, Image.Image] = {}
        self.manufacturer._set_value(value='Škoda')  # pylint: disable=protected-access


class SkodaElectricVehicle(ElectricVehicle, SkodaVehicle):
    """
    Represents a Skoda electric vehicle.
    """
    def __init__(self, vin: Optional[str] = None, garage: Optional[Garage] = None, managing_connector: Optional[BaseConnector] = None,
                 origin: Optional[SkodaVehicle] = None) -> None:
        if origin is not None:
            super().__init__(garage=garage, origin=origin)
            if isinstance(origin, ElectricVehicle):
                self.charging: Charging = SkodaCharging(vehicle=self, origin=origin.charging)
            else:
                self.charging: Charging = SkodaCharging(vehicle=self, origin=self.charging)
        else:
            super().__init__(vin=vin, garage=garage, managing_connector=managing_connector)
            self.charging: Charging = SkodaCharging(vehicle=self, origin=self.charging)


class SkodaCombustionVehicle(CombustionVehicle, SkodaVehicle):
    """
    Represents a Skoda combustion vehicle.
    """
    def __init__(self, vin: Optional[str] = None, garage: Optional[Garage] = None, managing_connector: Optional[BaseConnector] = None,
                 origin: Optional[SkodaVehicle] = None) -> None:
        if origin is not None:
            super().__init__(garage=garage, origin=origin)
        else:
            super().__init__(vin=vin, garage=garage, managing_connector=managing_connector)


class SkodaHybridVehicle(HybridVehicle, SkodaVehicle):
    """
    Represents a Skoda hybrid vehicle.
    """
    def __init__(self, vin: Optional[str] = None, garage: Optional[Garage] = None, managing_connector: Optional[BaseConnector] = None,
                 origin: Optional[SkodaVehicle] = None) -> None:
        if origin is not None:
            super().__init__(garage=garage, origin=origin)
        else:
            super().__init__(vin=vin, garage=garage, managing_connector=managing_connector)
