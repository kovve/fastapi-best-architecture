from fastapi import APIRouter

from backend.app.customer.api.v1.contract import router as contract_router
from backend.app.customer.api.v1.enterprise import router as enterprise_router
from backend.app.customer.api.v1.financial import router as financial_router
from backend.app.customer.api.v1.other_record import router as other_record_router
from backend.app.customer.api.v1.patent import router as patent_router
from backend.app.customer.api.v1.project import router as project_router
from backend.app.customer.api.v1.service_fee import router as service_fee_router

router = APIRouter()

router.include_router(enterprise_router, prefix='/enterprises', tags=['客户企业'])
router.include_router(contract_router, prefix='/contracts', tags=['客户合同'])
router.include_router(financial_router, prefix='/financials', tags=['客户财务'])
router.include_router(project_router, prefix='/projects', tags=['申报项目'])
router.include_router(service_fee_router, prefix='/service-fees', tags=['服务费'])
router.include_router(patent_router, prefix='/patents', tags=['专利信息'])
router.include_router(other_record_router, prefix='/other-records', tags=['其他记录'])
