from dependency_injector import containers, providers
from core.infrastructure.database.database_client import DatabaseClient
from core.infrastructure.supabase.supabase_facade import SupabaseFacade
from core.infrastructure.repositories.grooming_session_repository import GroomingSessionRepository
from core.infrastructure.repositories.estimation_turn_repository import EstimationTurnRepository
from core.infrastructure.repositories.user_repository import UserRepository
from core.services.grooming_session_service import GroomingSessionService
from core.services.user_service import UserService


class Container(containers.DeclarativeContainer):
    # Infrastructure
    database_client = providers.Singleton(DatabaseClient)
    supabase_facade = providers.Singleton(SupabaseFacade)
    
    # Repositories
    grooming_session_repository = providers.Factory(
        GroomingSessionRepository,
        db_client=database_client
    )
    
    user_repository = providers.Factory(
        UserRepository,
        db_client=database_client
    )
    
    estimation_turn_repository = providers.Factory(
        EstimationTurnRepository,
        db_client=database_client
    )
    
    # Services
    grooming_session_service = providers.Factory(
        GroomingSessionService,
        grooming_session_repository=grooming_session_repository,
        estimation_turn_repository=estimation_turn_repository,
        user_repository=user_repository,
        supabase=supabase_facade
    )
    
    user_service = providers.Factory(
        UserService,
        user_repository=user_repository,
        supabase=supabase_facade
    )