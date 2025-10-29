class QueryConversion(Base):
   __tablename__ = 'query_conversions'
   id = Column(Integer, primary_key=True)
   asset_title = Column(String, nullable=False)
   type = Column(String, nullable=False) 
   source_format = Column(String, nullable=False)      # 'Graphite'
   target_format = Column(String, nullable=False)      # 'PromQL'
   source_query = Column(Text, nullable=False)
   target_query = Column(Text, nullable=False)
   customer_name = Column(Text, nullable=False)
   explanation = Column(Text) # aka description
   added_by = Column(String)
   added_on = Column(DateTime, default=datetime.datetime.utcnow)


class Guidance(Base):
   __tablename__ = 'guidance' #question migration, 
   id = Column(Integer, primary_key=True)
   title = Column(String, nullable=False)
   source_format = Column(String, nullable=False)      # 'Graphite'
   target_format = Column(String, nullable=False)      # 'PromQL'
   customer_name = Column(Text, nullable=False)
   description = Column(Text, nullable=False)
   last_updated = Column(DateTime, default=datetime.datetime.utcnow)
   updated_by = Column(String)


class MessageResponse(Base):
   __tablename__ = 'message_responses'
   id = Column(Integer, primary_key=True)
   issue_topic = Column(String, nullable=False)            # e.g., 'Migration Error', 'HPA Scaling'
   message = Column(Text, nullable=False)
   customer_name = Column(Text, nullable=False)
   responder = Column(String)
   responder_role = Column(String, nullable=False)
   channel = Column(String)
   timestamp = Column(DateTime, default=datetime.datetime.utcnow)
   tags = Column(Text)                                     # Optional CSV of tags/keywords


class Standardization(Base):
   __tablename__ = 'standardizations'
   id = Column(Integer, primary_key=True)
   item = Column(String, nullable=False)                   # e.g., 'Always use rate() for APM metric'
   details = Column(Text)
   status = Column(String, default='draft')                # 'draft', 'in-review', 'final'
   last_updated = Column(DateTime, default=datetime.datetime.utcnow)
   updated_by = Column(String)
   related_guidance_id = Column(Integer, ForeignKey('guidance.id'))


# For flexible tagging/search
class Tag(Base):
   __tablename__ = 'tags'
   id = Column(Integer, primary_key=True)
   label = Column(String, unique=True)