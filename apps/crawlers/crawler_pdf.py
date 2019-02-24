# coding: utf-8
import os, time, zipfile
from decimal import Decimal
from datetime import date
from django.conf import settings
from .common import CrawlerUtils
# from vsales.apps.payments.models import PaymentCondition
# from vsales.apps.profiles.models import PERSON_TYPE


class CrawlerPDF(CrawlerUtils):

    def login(self, username, password):
        self.goTo('https://www.berkley.com.br/Institucional')
        try:
            time.sleep(15)
            self.write_input('//*[@id="UserUsername"]', username)
            self.write_input('//*[@id="UserPassword"]', password)
            self.click('//*[@id="UserLoginForm"]/button')
            self.logged = True
        except:
            self.login(username=username, password=password)

    def choose_segment_name(self, name):
        self.click('//*[@id="content"]/div[1]/div/div/div[3]/div[1]/div[1]/div')
        self.write_select('//*[@id="produtoCotar"]', name)
        self.click('//*[@id="modalNovaCotacao"]/div[2]/div/div[3]/button[2]')

    def type_proposal_data(self, proposal):
        self.click('//*[@id="subGrupos"]/fieldset[4]')
        self.write_select('//*[@id="form_subgrupo_3"]/label/select', 'Anual')
        self.write_input('//*[@id="form_subgrupo_3"]/label/input[@name="mov_cotacao_inicio_288"]',
                         proposal.accepted_at.strftime('%d/%m/%Y'))
        self.click('//*[@id="subGrupos"]/fieldset[4]')
        # self.click('//*[@id="form_subgrupo_3"]/label/input[@name="mov_cotacao_inicio_288"]')
        # self.click('//*[@id="form_subgrupo_3"]/label/input[@name="mov_cotacao_inicio_288"]')
        # self.click('//*[@id="form_subgrupo_3"]/label/input[@name="mov_cotacao_inicio_288"]')
        # time.sleep(5)
        # self.click('//*[@class="ui-datepicker-calendar"]/tbody/tr/td[contains(@class, "ui-datepicker-today")]')
        # # self.click('//*[@id="ui-datepicker-div"]/table/tbody/tr[2]/td[5]')
        self.click('//*[@id="form_subgrupo_3"]/button[@type="submit"]')

    def type_customer_data(self, request):
        self.click('//*[@id="subGrupos"]/fieldset[5]')
        self.write_input('//*[@id="form_subgrupo_4"]/label/input[@name="seguradoCpfCnpj_556"]',
                         request.customer.document.replace('.', '').replace('-', ''))
        self.click('//*[@id="form_subgrupo_4"]/label/a[@class="busca btnBusca btnBuscaRegraPos"]')
        time.sleep(10)
        if self.element_exists('//*[@id="resultadoAjaxConteudo"]/b/h3'):
            raise Exception('cpf invalido')
        elif self.element_exists('//*[@id="cadastroPessoa"]'):
            self.write_input('//*[@id="nr_cnpj_cpf"]', request.customer.document)
            self.write_input('//*[@id="cadastroPessoa"]/label/input[@id="nome"]', request.customer.name)
            if request.customer.entity_type == PERSON_TYPE:
                self.click('//*[@id="cadastroPessoa"]/div/label/input[@id="pessoaFisica"]')
                if request.customer.birth:
                    self.write_input('//*[@id="cadastroPessoa"]/label/input[@id="dataNascimento"]',
                                     request.customer.birth.strftime('%d/%m/%Y'))
                self.click('//*[@id="cadastroPessoa"]')

            else:
                self.click('//*[@id="cadastroPessoa"]/div/label/input[@id="pessoaJuridica"]')
            self.click('//*[@id="cadastroPessoa"]/button[@type="submit"]')

            time.sleep(3)
            self.wait_until_hide_element('//*[@id="procesandoForm"]/p[2]', time=60)
            time.sleep(3)
            if self.element_exists('//*[@id="erroAjax"]'):
                try:
                    self.click('/html/body/div[13]/div[1]/a')
                except:
                    pass
                time.sleep(3)
                self.write_input('//*[@id="form_subgrupo_4"]/label/input[@name="seguradoCpfCnpj_556"]',
                                 request.customer.document.replace('.', '').replace('-', ''))
                self.click('//*[@id="form_subgrupo_4"]/label/a[@class="busca btnBusca btnBuscaRegraPos"]')
                time.sleep(10)

        time.sleep(15)
        if not self.element_exists('/html/body/div[2]/div[2]/fieldset[5]/div/form/label[3]/select/option'):
            self.click('//*[@id="form_subgrupo_4"]/label/button[@id="cadastrarEndereco"]')
            self.click('//*[@id="cadastroEndereco"]/div/label/input[@value="5"]')
            self.write_input('//*[@id="cadastroEndereco"]/label/input[@id="endereco_cep"]',
                             request.customer.address.postal_code)
            self.click('//*[@id="cadastroEndereco"]/label/a[@id="procura_cep"]')
            if not self.element_has_value('//*[@id="endereco_logradouro"]'):
                self.write_input('//*[@id="endereco_logradouro"]', request.customer.address.street)
                self.write_input('//*[@id="endereco_bairro"]', request.customer.address.district)
                self.write_select('//*[@id="endereco_estado"]', request.customer.address.state.name)
                try:
                    self.write_select('//*[@id="endereco_cidade"]', request.customer.address.city.name)
                except:
                    self.write_select_by_index('//*[@id="endereco_cidade"]', 2)
            self.write_input('//*[@id="cadastroEndereco"]/label/input[@id="endereco_numero"]',
                             request.customer.address.number)
            self.click('//*[@id="cadastroEndereco"]/button[@type="submit"]')
        self.click('//*[@id="form_subgrupo_4"]/button[@type="submit"]')

    def type_quiz_data(self, request):
        if request.quiz:
            self.click('//*[@id="subGrupos"]/fieldset[6]')
            p1 = request.quiz.questions.filter(slug='p1').first()
            a1 = p1.question_answers.filter(request=request, quiz=request.quiz).first()
            c1 = a1.choices.first()
            if c1:
                c1.text = u'NÃO' if c1.text.upper() == 'N/A' else c1.text.upper()
                self.write_select('//*[@id="form_subgrupo_5"]/label/select[@id="quest_3"]', u' %s' % c1.text)
            aa1 = a1.annotations.first()
            self.write_input('//*[@id="form_subgrupo_5"]/label/input[@id="776"]', aa1.text if aa1 else '')

            p2 = request.quiz.questions.filter(slug='p2').first()
            a2 = p2.question_answers.filter(request=request, quiz=request.quiz).first()

            locations = ''
            for c2 in a2.choices.all():
                locations += '%s, ' % c2.text

            self.write_input('//*[@id="form_subgrupo_5"]/label/input[@id="777"]', locations)

            p3 = request.quiz.questions.filter(slug='p3').first()
            a3 = p3.question_answers.filter(request=request, quiz=request.quiz).first()
            c3 = a3.choices.first()
            if c3:
                if c3.text == '1 a 2':
                    value = '2 VEZES NA SEMANA'
                elif c3.text == '3 a 4':
                    value = '4 VEZES NA SEMANA'
                elif c3.text == '5 a 7':
                    value = '7 VEZES NA SEMANA'
                else:
                    value = '1 VEZ NA SEMANA'
                self.write_select('//*[@id="form_subgrupo_5"]/label/select[@id="778"]', value)

            p4 = request.quiz.questions.filter(slug='p4').first()
            a4 = p4.question_answers.filter(request=request, quiz=request.quiz).first()
            c4 = a4.choices.first()
            if c4:
                c4.text = 'NÃO' if c4.text.upper() == 'N/A' else c4.text.upper()
                self.write_select('//*[@id="form_subgrupo_5"]/label/select[@id="quest_6"]', ' %s' % c4.text)
            aa4 = a4.annotations.first()
            self.write_input('//*[@id="form_subgrupo_5"]/label/input[@id="779"]', aa4.text if aa4 else '')
            self.write_select('//*[@id="form_subgrupo_5"]/label/select[@id="quest_91"]', ' Não')
            # self.write_input('//*[@id="form_subgrupo_5"]/label/textarea[@id="2570"]', 'Eu mesmo')
            self.click('//*[@id="form_subgrupo_5"]/button[@type="submit"]')

    def send_proposal(self, request, proposal):
        if not self.logged:
            # LOGIN
            self.login(settings.BERKLEY_LOGIN_DEFAULT, settings.BERKLEY_PASSWORD_DEFAULT)

            time.sleep(10)

            # CHECKING FOR MODAL
            if self.element_is_clickable('//*[@id="dialog"]/button'):
                self.click('//*[@id="dialog"]/button')

            # CHOOSING BIKE OPTION
            self.choose_segment_name('Bike')

            time.sleep(50)

        # GO TO NEW QUOTATION FORM
        self.goTo('https://www.berkley.com.br/cotador/Produto/14/Cotacoes?SubCorretor=0')
        self.goTo('https://www.berkley.com.br/cotador/Produto/14/Cotacoes?SubCorretor=0')
        time.sleep(20)
        self.click('//*[@id="frmCotacao"]/a', 40)
        time.sleep(20)

        # self.click('//*[@id="resultados"]/table/tbody/tr/td/input[@value="319436"]')  # remove this
        # self.click('//*[@class="btn-editar"]')  # remove this

        # QUOTATION DESCRIPTION
        p = PaymentCondition.objects.filter(insurer=proposal.insurer, segment=request.segment).first()
        liquid = proposal.price.value / Decimal(7.38 / 100 + 1)
        value = p.calculate_installment_single_value(proposal.price.value, proposal.installments)
        self.write_input('//*[@id="form_subgrupo_0"]/label/textarea',
                         u'VNZ\n Prêmio Líquido R$ %.2f\n Prêmio Total R$ %.2f \n Forma de pagamento – %d x R$ %.2f \n Boletos com vencimento de 5 dias após a emissão \n Comissão – %d %%' % (
                         liquid, proposal.price.value, proposal.installments, value, int(proposal.commission)), 80)
        self.click('//*[@id="form_subgrupo_0"]/button[@type="submit"]')

        # OPPORTUNITY DATA
        self.type_proposal_data(proposal)

        # CUSTOMER DATA
        self.type_customer_data(request)

        time.sleep(6)

        # QUIZ
        self.type_quiz_data(request)

        time.sleep(6)

        # RISCO E COBERTURA
        for product in proposal.products.all():
            self.click('//*[@id="subGrupos"]/fieldset[7]', 60)
            self.click('//*[@id="subGrupoRisco"]/fieldset', 60)
            self.click('//*[@id="form_subgrupo_8"]/table/tbody/tr/td/a[@class="coberturasTable-adicionais-btn"]', 60)
            self.click('//*[@id="item-241"]/td/div/div/div[2]/button')
            self.click('//*[@id="adicionarItem"]/tbody/tr[1]/td/label/input')
            self.write_input('//*[@id="form_item_1"]/label/input[@id="valorItem_322"]', '%.2f' % product.item.price.value)
            if product.item.chassis:
                self.write_input('//*[@id="form_item_1"]/label/input[@id="323"]', product.item.chassis)
            self.write_input('//*[@id="form_item_1"]/label/input[@id="324"]', product.item.year)
            self.write_input('//*[@id="form_item_1"]/label/input[@id="325"]', product.item.model.name)
            self.click('//*[@id="form_item_1"]/button[@type="submit"]')

            # TODO: colocar host do servidor
            # url = urllib2.urlopen('http://%s/api/v1/proposals/pdf/%s/' % (settings.HOST_BASE, proposal.hash))
            # url = urllib2.urlopen('http://localhost:8000/api/v1/proposals/pdf/%s/' % proposal.hash)
            zipf = zipfile.ZipFile(os.path.join(settings.BASE_DIR, 'tmp.zip'), 'w', zipfile.ZIP_DEFLATED)
            zipf.writestr('proposal.pdf', url.read())
            zipf.close()

            # TODO: colocar path absoluto do servidor
            # self.write_input('//*[@id="fileuploadZip"]', '/Users/victorluna/projetos/vsales/Sales-Server/api/%s' % zipf.filename)
            self.write_input('//*[@id="fileuploadZip"]', os.path.join(settings.BASE_DIR, zipf.filename))
            time.sleep(30)

        time.sleep(10)

        self.click('//*[@id="calcular"]', 60)

        time.sleep(25)

        # PAGAMENTOS
        self.click('//*[@id="subGrupos"]/fieldset[8]')
        time.sleep(3)
        if self.element_exists('/html/body/div[2]/div[2]/fieldset[8]/div/div/form/table/tbody/tr[1]'):
            self.click_multiple('#formFormaPagamentoCotacao .resultadosTable input:checked[type="checkbox"]')
            self.click('//*[@id="formFormaPagamentoCotacao"]/table/tbody/tr/td/input[@value="1"]')
            self.click('//*[@id="formFormaPagamentoCotacao"]/button[@type="submit"]')

        self.click('//*[@id="salvarcotacao"]')

        time.sleep(10)
        if self.element_exists('//*[@id="dummybodyid"]/div[16]/div[3]/div/button'):
            self.click('//*[@id="dummybodyid"]/div[16]/div[3]/div/button')

        try:
            os.remove(os.path.join(settings.BASE_DIR, zipf.filename))
        except OSError:
            pass

        # print 'ok'
