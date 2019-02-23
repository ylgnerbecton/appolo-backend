from django.db import models

class State(models.Model):
    uf = models.CharField('Estado', max_length=2)
    description = models.CharField(max_length=100, blank=True, null=True)
    cod_ibge = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "Estado"

    def __str__(self):
        return self.uf


class City(models.Model):
    name = models.CharField('Cidade', max_length=100, blank=True, null=True, db_index=True)
    state = models.ForeignKey(State, max_length=2, blank=True, null=True, on_delete=models.DO_NOTHING)
    latitude = models.DecimalField(max_digits=14, decimal_places=12, blank=True, null=True)
    longitude = models.DecimalField(max_digits=14, decimal_places=12, blank=True, null=True)
    cod_ibge = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "Cidade"

    def __str__(self):
        return self.name


class Neighborhood(models.Model):
    description = models.CharField('Bairro', max_length=100, blank=True, null=True)
    city = models.ForeignKey(City, blank=True, null=True, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "Bairro"

    def __str__(self):
        return self.description


class Place(models.Model):
    zip_code = models.CharField('CEP', max_length=10)
    description = models.CharField(max_length=200, blank=True, null=True)
    place_type = models.CharField(max_length=80, blank=True, null=True)
    latitude = models.DecimalField(max_digits=14, decimal_places=12, blank=True, null=True)
    longitude = models.DecimalField(max_digits=14, decimal_places=12, blank=True, null=True)
    city = models.ForeignKey(City,blank=True, null=True, on_delete=models.DO_NOTHING)
    neighborhood = models.ForeignKey(Neighborhood, blank=True, null=True, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "Localidade"

    def __str__(self):
        return self.zip_code

    def get_zipcode_formated(self):
        return self.zip_code.replace('.','').replace('-','')


class Address(models.Model):
    place = models.ForeignKey(Place, on_delete=models.DO_NOTHING)
    street = models.CharField('Rua', max_length=300)
    number = models.CharField('Número', max_length=20, null=True, blank=True)
    complement = models.CharField('Complemento', max_length=100, null=True, blank=True)
    reference_point = models.CharField('Ponto de referência', max_length=100, null=True, blank=True)
    latitude = models.DecimalField(max_digits=14, decimal_places=12, blank=True, null=True)
    longitude = models.DecimalField(max_digits=14, decimal_places=12, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING)
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.DO_NOTHING)
    state = models.ForeignKey(State, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "Endereço"

    def __str__(self):
        return '{}, {}, {}, {} - {}'.format(self.street, self.number, self.neighborhood, self.city, self.state)


class Term(models.Model):
    description = models.CharField('Descrição', max_length=200)
    document_file = models.FileField('Termo', blank=True, null=True)

    class Meta:
        verbose_name = "Termo de uso"
    
    def __str__(self):
        return '{}'.format(self.description)


class Company(models.Model):
    name = models.CharField('Razão Social', max_length=100, blank=True, null=True)
    fantasy = models.CharField('Nome Fantasia', max_length=100, blank=True, null=True)
    address = models.ForeignKey(Address, on_delete=models.DO_NOTHING, blank=True, null=True)
    cnpj = models.CharField('CNPJ', max_length=22, blank=True, null=True)
    tse_date = models.DateField('Data de registro no TSE', blank=True, null=True)
    comprovant = models.FileField('Documentos', blank=True, null=True)
    url = models.URLField('URL Website', blank=True, null=True)

    class Meta:
        verbose_name = "Empresa"

    def __str__(self):
        return '{} - {}'.format(self.cnpj, self.name)
