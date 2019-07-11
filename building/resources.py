from import_export import resources, widgets, fields
from .models import Building, Meter, Energy
import logging
logger = logging.getLogger(__name__)

class BaseResource(resources.ModelResource):
    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        for i, h in enumerate(dataset.headers):
            dataset.headers[i] = h.encode('utf-8').decode('utf-8-sig')

        
class BuildingsResource(BaseResource):

    # def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        # Remove the blank data
        # row = len(dataset) - 1
        # while(row >= 0):
        #     if dataset[row][0].strip() == "" or dataset[row][1].strip() == "":
        #         del dataset[row]
        #     row -= 1

    class Meta:
        model = Building
        skip_unchanged = True
        report_skipped = False
        fields = ('id', 'name',)
        clean_model_instances = True


class MeterResource(BaseResource):

    # Mapping building_id column to building field in the model.
    building = fields.Field(
        column_name='building_id',
        attribute='building',
        widget=widgets.ForeignKeyWidget(Building))

    class Meta:
        model = Meter
        skip_unchanged = True
        report_skipped = False
        fields = ('building', 'id', 'fuel', 'unit')
        clean_model_instances = True


class EnergyResource(BaseResource):
    # def __init__(self):
    #     self.to_create = []
    #     super()

    # def after_import(self, dataset, result, using_transactions, dry_run, **kwargs):
    #     from itertools import islice
    #     batch_size = 100
    #     while True:
    #         batch = list(islice(self.to_create, batch_size))
    #         if not batch:
    #             break
    #         Energy.objects.bulk_create(batch, batch_size, ignore_conflicts=True)




    # def import_row(self, row, instance_loader, using_transactions=True, dry_run=False, **kwargs):
    #     row_result = self.get_row_result_class()()
    #     instance_loader = self._meta.instance_loader_class(self, dataset)

    #     instance, new = self.get_or_init_instance(instance_loader, row)
    #     original = deepcopy(instance)

    #     try:
    #         self.import_obj(instance, row, dry_run)
    #     except ValidationError as e:
    #         # Validation errors from import_obj() are passed on to
    #         # validate_instance(), where they can be combined with model
    #         # instance validation errors if necessary
    #         import_validation_errors = e.update_error_dict(import_validation_errors)
    #     self.validate_instance(instance, import_validation_errors)

    #     if self.skip_row(instance, original):
    #         row_result.import_type = RowResult.IMPORT_TYPE_SKIP
    #     else:
    #         self.validate_instance(instance, import_validation_errors)
    #         energy_objects.append(instance)

    #     return row_result, instance
                   


    meter = fields.Field(
        column_name='meter_id',
        attribute='meter',
        widget=widgets.ForeignKeyWidget(Meter))


    class Meta:
        model = Energy
        skip_unchanged = True
        report_skipped = False
        exclude = ('id',)
        import_id_fields = []
        fields = ('meter_id', 'consumption', 'reading_date_time')
        clean_model_instances = True