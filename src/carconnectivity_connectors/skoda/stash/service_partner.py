"""Module for service partner classes."""
from __future__ import annotations
from typing import TYPE_CHECKING

from carconnectivity.objects import GenericObject
from carconnectivity.attributes import StringAttribute

if TYPE_CHECKING:
    from typing import Optional


class ServicePartner(GenericObject):
    """
    Represents the service partner information for a Skoda vehicle.
    """
    
    def __init__(self, parent: Optional[GenericObject] = None, origin: Optional[ServicePartner] = None) -> None:
        """
        Initialize ServicePartner object.
        
        Args:
            parent: Parent object (typically a SkodaVehicle)
            origin: Original ServicePartner object to copy from
        """
        super().__init__(object_id='service_partner', parent=parent)
        
        if origin is not None:
            # Copy from existing ServicePartner object
            self._copy_attributes_from_origin(origin)
        else:
            # Initialize new ServicePartner object
            self.service_partner_id = StringAttribute('service_partner_id', parent=self, tags={'connector_custom'})
    
    def _copy_attributes_from_origin(self, origin: ServicePartner) -> None:
        """
        Copy attributes from another ServicePartner object.
        
        Args:
            origin: The ServicePartner object to copy from
        """
        try:
            self.service_partner_id = StringAttribute('service_partner_id', parent=self, tags={'connector_custom'})
            if hasattr(origin, 'service_partner_id') and origin.service_partner_id.value is not None:
                self.service_partner_id._set_value(origin.service_partner_id.value)  # pylint: disable=protected-access
        except Exception:
            # Best effort: initialize with empty values if copying fails
            self.service_partner_id = StringAttribute('service_partner_id', parent=self, tags={'connector_custom'})
