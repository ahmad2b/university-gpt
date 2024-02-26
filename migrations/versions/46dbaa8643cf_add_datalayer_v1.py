"""Add DataLayer v1

Revision ID: 46dbaa8643cf
Revises: 
Create Date: 2024-02-26 02:52:37.136842

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '46dbaa8643cf'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('student',
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('student_id')
    )
    op.create_table('topic',
    sa.Column('title', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['parent_id'], ['topic.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_topic_id'), 'topic', ['id'], unique=False)
    op.create_index(op.f('ix_topic_title'), 'topic', ['title'], unique=False)
    op.create_table('university',
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('university_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('university_id')
    )
    op.create_table('content',
    sa.Column('topic_id', sa.Integer(), nullable=True),
    sa.Column('content_text', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['topic_id'], ['topic.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_content_id'), 'content', ['id'], unique=False)
    op.create_index(op.f('ix_content_topic_id'), 'content', ['topic_id'], unique=False)
    op.create_table('program',
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('program_id', sa.Integer(), nullable=False),
    sa.Column('university_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['university_id'], ['university.university_id'], ),
    sa.PrimaryKeyConstraint('program_id')
    )
    op.create_table('questionbank',
    sa.Column('question_text', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.Column('points', sa.Integer(), nullable=False),
    sa.Column('difficulty', sa.Enum('easy', 'medium', 'hard', name='questiondifficultyenum'), nullable=False),
    sa.Column('topic_id', sa.Integer(), nullable=False),
    sa.Column('question_type', sa.Enum('single_select_mcq', 'multiple_select_mcq', name='questiontypeenum'), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['topic_id'], ['topic.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('course',
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.Column('program_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['program_id'], ['program.program_id'], ),
    sa.PrimaryKeyConstraint('course_id')
    )
    op.create_table('mcqoption',
    sa.Column('option_text', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('is_correct', sa.Boolean(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['question_id'], ['questionbank.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('quiz',
    sa.Column('title', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('duration', sa.Interval(), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.Column('instructions', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('total_points', sa.Integer(), nullable=False),
    sa.Column('quiz_key', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['course.course_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_quiz_id'), 'quiz', ['id'], unique=False)
    op.create_index(op.f('ix_quiz_title'), 'quiz', ['title'], unique=False)
    op.create_table('answersheet',
    sa.Column('quiz_id', sa.Integer(), nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('answerJSON', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('quiz_start_time', sa.DateTime(), nullable=False),
    sa.Column('quiz_end_time', sa.DateTime(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['quiz_id'], ['quiz.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['student.student_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('quizquestion',
    sa.Column('quiz_id', sa.Integer(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.Column('instructor_comment', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.ForeignKeyConstraint(['question_id'], ['questionbank.id'], ),
    sa.ForeignKeyConstraint(['quiz_id'], ['quiz.id'], ),
    sa.PrimaryKeyConstraint('quiz_id', 'question_id')
    )
    op.create_index(op.f('ix_quizquestion_question_id'), 'quizquestion', ['question_id'], unique=False)
    op.create_index(op.f('ix_quizquestion_quiz_id'), 'quizquestion', ['quiz_id'], unique=False)
    op.create_table('quiztopic',
    sa.Column('quiz_id', sa.Integer(), nullable=False),
    sa.Column('topic_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['quiz_id'], ['quiz.id'], ),
    sa.ForeignKeyConstraint(['topic_id'], ['topic.id'], ),
    sa.PrimaryKeyConstraint('quiz_id', 'topic_id')
    )
    op.create_index(op.f('ix_quiztopic_quiz_id'), 'quiztopic', ['quiz_id'], unique=False)
    op.create_index(op.f('ix_quiztopic_topic_id'), 'quiztopic', ['topic_id'], unique=False)
    op.create_table('result',
    sa.Column('answer_sheet_id', sa.Integer(), nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('quiz_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('total_marks', sa.Integer(), nullable=False),
    sa.Column('obtained_marks', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['answer_sheet_id'], ['quiz.id'], ),
    sa.ForeignKeyConstraint(['quiz_id'], ['quiz.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['student.student_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('result')
    op.drop_index(op.f('ix_quiztopic_topic_id'), table_name='quiztopic')
    op.drop_index(op.f('ix_quiztopic_quiz_id'), table_name='quiztopic')
    op.drop_table('quiztopic')
    op.drop_index(op.f('ix_quizquestion_quiz_id'), table_name='quizquestion')
    op.drop_index(op.f('ix_quizquestion_question_id'), table_name='quizquestion')
    op.drop_table('quizquestion')
    op.drop_table('answersheet')
    op.drop_index(op.f('ix_quiz_title'), table_name='quiz')
    op.drop_index(op.f('ix_quiz_id'), table_name='quiz')
    op.drop_table('quiz')
    op.drop_table('mcqoption')
    op.drop_table('course')
    op.drop_table('questionbank')
    op.drop_table('program')
    op.drop_index(op.f('ix_content_topic_id'), table_name='content')
    op.drop_index(op.f('ix_content_id'), table_name='content')
    op.drop_table('content')
    op.drop_table('university')
    op.drop_index(op.f('ix_topic_title'), table_name='topic')
    op.drop_index(op.f('ix_topic_id'), table_name='topic')
    op.drop_table('topic')
    op.drop_table('student')
    # ### end Alembic commands ###